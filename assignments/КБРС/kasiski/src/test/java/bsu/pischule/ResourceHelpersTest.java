package bsu.pischule;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ResourceHelpersTest {

    @Test
    void loadLanguage() {
        var lang = ResourceHelpers.loadLetterFrequency("russian");
        assertNotNull(lang);
        assertTrue(lang.size() > 10);
    }

    @Test
    void loadAlphabet() {
        var alphabet = ResourceHelpers.loadAlphabet("russian");
        System.out.println(alphabet);
        assertTrue(alphabet.startsWith("а"));
        assertTrue(alphabet.endsWith("я"));
    }
}