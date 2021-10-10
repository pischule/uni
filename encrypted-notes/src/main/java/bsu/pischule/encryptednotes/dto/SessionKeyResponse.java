package bsu.pischule.encryptednotes.dto;

import lombok.*;

@AllArgsConstructor
@Builder
@NoArgsConstructor(access = AccessLevel.PRIVATE)
@Data
public class SessionKeyResponse {
    private String encryptedSessionKey;
}
