package bsu.pischule.encryptednotes.dto;

import lombok.Data;

@Data
public class CreateEncryptedNoteRequest {
    private byte[] encryptedNote;
    private byte[] iv;
}
