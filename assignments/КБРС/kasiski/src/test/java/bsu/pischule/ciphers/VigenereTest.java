package bsu.pischule.ciphers;

import org.junit.jupiter.api.Test;

import static bsu.pischule.ResourceHelpers.loadAlphabet;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class VigenereTest {
    @Test
    void encrypt() {
        var vigenere = new Vigenere(loadAlphabet("english"), "mouse");
        var result = vigenere.encrypt("Cryptography AND data Security");
        assertEquals("Ofshxaulsttm SRP xsxm Mwggfclc", result);
    }

    @Test
    void decrypt() {
        var vigenere = new Vigenere(loadAlphabet("english"), "mouse");
        var result = vigenere.decrypt("Ofshxaulsttm SRP xsxm Mwggfclc");
        assertEquals("Cryptography AND data Security", result);
    }

}
