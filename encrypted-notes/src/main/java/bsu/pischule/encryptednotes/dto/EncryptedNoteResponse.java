package bsu.pischule.encryptednotes.dto;

import lombok.*;

@AllArgsConstructor
@Builder
@NoArgsConstructor(access = AccessLevel.PRIVATE)
@Data
public class EncryptedNoteResponse {
    public String encryptedText;
    public String iv;
}
