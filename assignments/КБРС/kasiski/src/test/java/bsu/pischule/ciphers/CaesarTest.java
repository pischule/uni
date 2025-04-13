package bsu.pischule.ciphers;

import org.junit.jupiter.api.Test;

import static bsu.pischule.ResourceHelpers.loadAlphabet;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class CaesarTest {
    @Test
    void encrypt() {
        var caesar = new Caesar(loadAlphabet("english"), 3);
        var result = caesar.encrypt("dcode caesar");
        assertEquals("gfrgh fdhvdu", result);
    }

    @Test
    void decrypt() {
        var caesar = new Caesar(loadAlphabet("english"), 3);
        var result = caesar.decrypt("gfrgh fdhvdu");
        assertEquals("dcode caesar", result);
    }
}
