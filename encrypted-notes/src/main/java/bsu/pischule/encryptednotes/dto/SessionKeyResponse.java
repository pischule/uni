package bsu.pischule.encryptednotes.dto;

import java.util.UUID;

public record SessionKeyResponse(
        byte[] encryptedSessionKey,
        UUID sessionToken) {
}
