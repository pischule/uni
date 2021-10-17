package bsu.pischule.encryptednotes.controller;

import bsu.pischule.encryptednotes.dto.SessionKeyRequest;
import bsu.pischule.encryptednotes.dto.SessionKeyResponse;
import bsu.pischule.encryptednotes.service.UserService;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import javax.validation.Valid;

@CrossOrigin
@AllArgsConstructor
@RestController
public class SessionKeyController {
    private final UserService notesService;

    public SessionKeyResponse getSessionKey(@RequestBody @Valid SessionKeyRequest request) {
        return notesService.getSessionKey(request);
    }
}
