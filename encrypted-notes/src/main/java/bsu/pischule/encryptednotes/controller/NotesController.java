package bsu.pischule.encryptednotes.controller;

import bsu.pischule.encryptednotes.dto.EncryptedNoteResponse;
import bsu.pischule.encryptednotes.dto.SessionKeyRequest;
import bsu.pischule.encryptednotes.dto.SessionKeyResponse;
import bsu.pischule.encryptednotes.service.NotesService;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import javax.validation.Valid;

@AllArgsConstructor
@RestController
public class NotesController {
    private final NotesService notesService;

    @PostMapping("/api/login")
    public SessionKeyResponse getSessionKey(@RequestBody @Valid SessionKeyRequest request) {
        try {
            return notesService.getSessionKey(request);
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage());
        }
    }

    @GetMapping("/api/note")
    public EncryptedNoteResponse getEncryptedNote(@RequestParam Long noteId,
                                                  @RequestParam Long userId) {
        try {
            return notesService.getEncryptedNotes(noteId, userId);
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(
                    HttpStatus.NOT_FOUND, e.getMessage());
        }
    }
}
