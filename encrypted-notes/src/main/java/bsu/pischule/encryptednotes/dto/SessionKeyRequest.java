package bsu.pischule.encryptednotes.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Data
public class SessionKeyRequest {
    @NotBlank
    private String username;
    @NotNull
    private String password;
    @NotBlank
    private String publicKeyPem;
}
