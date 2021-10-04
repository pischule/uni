package bsu.pischule.encryptednotes.service;

import bsu.pischule.encryptednotes.dto.EncryptedNoteResponse;
import bsu.pischule.encryptednotes.dto.SessionKeyRequest;
import bsu.pischule.encryptednotes.dto.SessionKeyResponse;
import bsu.pischule.encryptednotes.entity.Note;
import bsu.pischule.encryptednotes.entity.User;
import bsu.pischule.encryptednotes.repository.NoteRepository;
import bsu.pischule.encryptednotes.repository.UserRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;

@AllArgsConstructor
@Service
public class NotesService {
    private final UserRepository userRepository;
    private final NoteRepository noteRepository;
    private final EncryptionService encryptionService;

    public SessionKeyResponse getSessionKey(SessionKeyRequest request) {
        User user = userRepository.findById(request.getUserId())
                .orElseThrow(() -> new IllegalArgumentException("User not found"));
        String sessionKey = encryptionService.generateSessionKey();
        user.setSessionKey(sessionKey);
        userRepository.save(user);
        return new SessionKeyResponse(user.getSessionKey());
    }

    public EncryptedNoteResponse getEncryptedNotes(Long noteId, Long userId) {
        Note note = noteRepository.findById(noteId)
                .orElseThrow(() -> new IllegalArgumentException("Note not found"));
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new IllegalArgumentException("User not found"));

        String sessionKey = Optional.ofNullable(user.getSessionKey())
                .orElseThrow(() -> new IllegalArgumentException("User doesn't have session key"));
        String plainText = note.getText();

        String encryptedText = encryptionService.encryptText(plainText, sessionKey);
        return new EncryptedNoteResponse(encryptedText);
    }
}
