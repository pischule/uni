package bsu.pischule.encryptednotes.dto;

public record CreateEncryptedNoteRequest(
        byte[] encryptedNote,
        byte[] iv
) {
}