package bsu.pischule.encryptednotes.controller;

import bsu.pischule.encryptednotes.dto.CreateEncryptedNoteRequest;
import bsu.pischule.encryptednotes.dto.EncryptedNoteResponse;
import bsu.pischule.encryptednotes.service.NotesService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;
import java.util.UUID;

@CrossOrigin
@RestController
@AllArgsConstructor
@RequestMapping("/api/note")
public class EncryptedNoteController {
    private final NotesService notesService;

    @GetMapping("/")
    public List<EncryptedNoteResponse> getNotes(@RequestHeader("Authorization") UUID sessionToken) {
        return notesService.getNotes(sessionToken);
    }

    @GetMapping("/{noteId}")
    public EncryptedNoteResponse getNote(@PathVariable UUID noteId,
                                         @RequestHeader("Authorization") UUID sessionToken) {
        return notesService.getNote(noteId, sessionToken);
    }

    @PostMapping("/")
    public EncryptedNoteResponse createNote(@RequestBody @Valid CreateEncryptedNoteRequest request,
                                            @RequestHeader("Authorization") UUID sessionToken) {
        return notesService.createNote(request, sessionToken);
    }

    @PutMapping("/{noteId}")
    public EncryptedNoteResponse updateNote(@PathVariable UUID noteId,
                                            @RequestBody @Valid CreateEncryptedNoteRequest request,
                                            @RequestHeader("Authorization") UUID sessionToken) {
        return notesService.updateNote(noteId, request, sessionToken);
    }

    @DeleteMapping("/{noteId}")
    public void deleteNote(@PathVariable UUID noteId,
                           @RequestHeader("Authorization") UUID sessionToken) {
        notesService.deleteNote(noteId, sessionToken);
    }
}
