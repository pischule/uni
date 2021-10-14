package bsu.pischule.encryptednotes.exception;

import javax.persistence.EntityNotFoundException;

public class DataNotFoundException extends EntityNotFoundException {
    public DataNotFoundException(String message) {
        super(message);
    }
}
