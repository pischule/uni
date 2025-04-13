package bsu.pischule.encryptednotes.dto;

import java.util.UUID;

public record EncryptedNoteResponse(
        UUID noteId,
        byte[] encryptedNote,
        byte[] iv
) {
}
