package bsu.pischule.encryptednotes.dto;

import lombok.Data;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;

@Data
public class SessionKeyRequest {
    @NotNull
    private Long userId;
    @NotBlank
    private String publicKey;
}
