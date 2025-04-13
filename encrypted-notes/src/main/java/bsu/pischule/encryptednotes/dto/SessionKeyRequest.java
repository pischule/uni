package bsu.pischule.encryptednotes.dto;

public record SessionKeyRequest(
        String username,
        String password,
        String publicKeyPem) {
}
