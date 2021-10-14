package bsu.pischule.encryptednotes.controller;

import bsu.pischule.encryptednotes.dto.SessionKeyRequest;
import bsu.pischule.encryptednotes.dto.SessionKeyResponse;
import bsu.pischule.encryptednotes.service.UserService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;

@CrossOrigin
@AllArgsConstructor
@RequestMapping("/api/session-key")
@RestController
public class SessionKeyController {
    private final UserService notesService;

    @PostMapping("/")
    public SessionKeyResponse getSessionKey(@RequestBody @Valid SessionKeyRequest request) {
        return notesService.getSessionKey(request);
    }

}
