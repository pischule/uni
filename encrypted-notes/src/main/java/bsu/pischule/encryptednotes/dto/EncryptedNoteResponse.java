package bsu.pischule.encryptednotes.dto;

import lombok.*;

@AllArgsConstructor
@Builder
@NoArgsConstructor(access = AccessLevel.PRIVATE)
@Data
public class EncryptedNoteResponse {
    public String encryptedNote;
    public String iv;
}
