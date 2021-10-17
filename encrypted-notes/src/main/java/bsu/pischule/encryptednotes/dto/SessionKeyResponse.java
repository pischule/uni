package bsu.pischule.encryptednotes.dto;

import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;


@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PRIVATE)
@Data
public class SessionKeyResponse {
    private byte[] encryptedSessionKey;
    private UUID sessionToken;
}
