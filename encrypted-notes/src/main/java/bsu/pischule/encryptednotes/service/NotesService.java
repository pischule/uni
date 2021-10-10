package bsu.pischule.encryptednotes.service;

import bsu.pischule.encryptednotes.dto.EncryptedNoteResponse;
import bsu.pischule.encryptednotes.dto.SessionKeyRequest;
import bsu.pischule.encryptednotes.dto.SessionKeyResponse;
import bsu.pischule.encryptednotes.entity.Note;
import bsu.pischule.encryptednotes.entity.User;
import bsu.pischule.encryptednotes.repository.NoteRepository;
import bsu.pischule.encryptednotes.repository.UserRepository;
import lombok.AllArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.transaction.Transactional;
import java.security.PublicKey;
import java.util.Base64;
import java.util.Optional;

@AllArgsConstructor
@Service
public class NotesService {
    private final UserRepository userRepository;
    private final NoteRepository noteRepository;
    private final EncryptionService encryptionService;

    @SneakyThrows
    @Transactional
    public SessionKeyResponse getSessionKey(SessionKeyRequest request) {
        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new IllegalArgumentException("User not found"));
        byte[] sessionKey = encryptionService.generateAesKey().getEncoded();
        user.setSessionKey(sessionKey);
        userRepository.save(user);
        PublicKey publicKey = encryptionService.readPublicKey(request.getPublicKeyPem());
        byte[] encryptedSessionKey = encryptionService.encryptRsa(sessionKey, publicKey);
        return SessionKeyResponse.builder()
                .encryptedSessionKey(Base64.getEncoder().encodeToString(encryptedSessionKey))
                .build();
    }

    @SneakyThrows
    public EncryptedNoteResponse getEncryptedNotes(Long noteId, Long userId) {
        Note note = noteRepository.findById(noteId)
                .orElseThrow(() -> new IllegalArgumentException("Note not found"));
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        byte[] sessionKey = Optional.ofNullable(user.getSessionKey())
                .orElseThrow(() -> new IllegalArgumentException("User doesn't have session key"));
        String plainText = note.getText();

        SecretKey key = encryptionService.fromBytes(user.getSessionKey());
        IvParameterSpec iv = encryptionService.generateIv();
        byte[] encryptedArray = encryptionService.encryptAes(plainText, key, iv);
        return EncryptedNoteResponse.builder()
                .encryptedText(Base64.getEncoder().encodeToString(encryptedArray))
                .iv(Base64.getEncoder().encodeToString(iv.getIV()))
                .build();
    }
}
