package bsu.pischule.encryptednotes.exception;

import lombok.Data;
import lombok.RequiredArgsConstructor;

import java.time.Instant;

@Data
@RequiredArgsConstructor
public class ErrorDetails {
    private final Instant timestamp = Instant.now();
    private final String message;
    private final String details;
}
