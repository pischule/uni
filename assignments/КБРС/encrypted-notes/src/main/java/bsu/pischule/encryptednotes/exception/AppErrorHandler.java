package bsu.pischule.encryptednotes.exception;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class AppErrorHandler {
    @ExceptionHandler(DataNotFoundException.class)
    public ResponseEntity<ErrorDetails> handleNotFound(DataNotFoundException e) {
        ErrorDetails errorDetails = new ErrorDetails(e.getMessage(), "data not found error");
        return new ResponseEntity<>(errorDetails, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(EncryptionException.class)
    public ResponseEntity<ErrorDetails> handleEncryptionError(EncryptionException e) {
        ErrorDetails errorDetails = new ErrorDetails(e.getMessage(), "encryption error");
        return new ResponseEntity<>(errorDetails, HttpStatus.INTERNAL_SERVER_ERROR);
    }

    @ExceptionHandler(AuthorizationException.class)
    public ResponseEntity<ErrorDetails> handleAuthorizationError(AuthorizationException e) {
        ErrorDetails errorDetails = new ErrorDetails(e.getMessage(), "authorization error");
        return new ResponseEntity<>(errorDetails, HttpStatus.FORBIDDEN);
    }
}
