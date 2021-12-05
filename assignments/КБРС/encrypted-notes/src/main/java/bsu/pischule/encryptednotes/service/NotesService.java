package bsu.pischule.encryptednotes.service;

import bsu.pischule.encryptednotes.dto.CreateEncryptedNoteRequest;
import bsu.pischule.encryptednotes.dto.EncryptedNoteResponse;
import bsu.pischule.encryptednotes.entity.Note;
import bsu.pischule.encryptednotes.entity.User;
import bsu.pischule.encryptednotes.exception.AuthorizationException;
import bsu.pischule.encryptednotes.repository.NoteRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.persistence.EntityNotFoundException;
import javax.transaction.Transactional;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@AllArgsConstructor
@Service
public class NotesService {
    private final UserService userService;
    private final NoteRepository noteRepository;
    private EncryptionService encryptionService;

    public EncryptedNoteResponse getNote(UUID noteId, UUID sessionToken) {
        User user = userService.getAndCheckUserBySessionToken(sessionToken);
        Note note = noteRepository.findByIdAndUser(noteId, user).orElseThrow(() -> new EntityNotFoundException("note not found"));
        return encryptNote(user, note);
    }

    public EncryptedNoteResponse createNote(CreateEncryptedNoteRequest request, UUID sessionToken) {
        User user = userService.getAndCheckUserBySessionToken(sessionToken);
        String text = decryptNote(user, request.encryptedNote(), request.iv());
        log.info("text: {}", text);
        Note note = new Note(null, user, text);
        noteRepository.save(note);
        return encryptNote(user, note);
    }

    public EncryptedNoteResponse updateNote(UUID noteId, CreateEncryptedNoteRequest request, UUID sessionToken) {
        User user = userService.getAndCheckUserBySessionToken(sessionToken);
        Note note = noteRepository.findByIdAndUser(noteId, user).orElseThrow(() -> new EntityNotFoundException("note not found"));
        String text = decryptNote(user, request.encryptedNote(), request.iv());
        note.setText(text);
        noteRepository.save(note);
        return encryptNote(user, note);
    }

    @Transactional
    public void deleteNote(UUID noteId, UUID sessionToken) {
        User user = userService.getAndCheckUserBySessionToken(sessionToken);
        noteRepository.deleteByIdAndUser(noteId, user);
    }

    public List<EncryptedNoteResponse> getNotes(UUID sessionToken) {
        User user = userService.getAndCheckUserBySessionToken(sessionToken);
        List<Note> notes = noteRepository.findAllByUser(user);
        return notes.stream().map(it -> encryptNote(user, it)).collect(Collectors.toList());
    }

    private String decryptNote(User user, byte[] encryptedText, byte[] ivBytes) {
        SecretKey sessionKey = encryptionService.getSessionKey(user.getSessionKey());
        IvParameterSpec iv = new IvParameterSpec(ivBytes);
        return encryptionService.decryptAes(encryptedText, sessionKey, iv);
    }

    private EncryptedNoteResponse encryptNote(User user, Note note) {
        if (Instant.now().isAfter(user.getSessionExpirationDate())) {
            throw new AuthorizationException("session key has expired");
        }
        SecretKey key = encryptionService.getSessionKey(user.getSessionKey());
        IvParameterSpec iv = encryptionService.generateIv();
        byte[] encryptedArray = encryptionService.encryptAes(note.getText(), key, iv);
        return new EncryptedNoteResponse(note.getId(), encryptedArray, iv.getIV());
    }
}
