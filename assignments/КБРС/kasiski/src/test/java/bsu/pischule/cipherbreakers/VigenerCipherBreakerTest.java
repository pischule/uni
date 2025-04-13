package bsu.pischule.cipherbreakers;

import bsu.pischule.ResourceHelpers;
import bsu.pischule.ciphers.Vigenere;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static org.junit.jupiter.api.Assertions.assertEquals;

class VigenerCipherBreakerTest {

    @ParameterizedTest
    @ValueSource(strings = {"это", "примеры", "паролей", "которыми", "я", "могу", "зашифровать", "текст"})
    void decryptTest(String password) {
        String text = """
                Жечь было наслаждением Какое то особое наслаждение видеть как огонь пожирает вещи как они чернеют и меняются Медный наконечник брандспойта зажат в кулаках громадный питон изрыгает на мир ядовитую струю керосина кровь стучит в висках а руки кажутся руками диковинного дирижера исполняющего симфонию огня и разрушения превращая в пепел изорванные обуглившиеся страницы истории Символический шлем украшенный цифрой  низко надвинут на лоб; глаза сверкают оранжевым пламенем при мысли о том что должно сейчас произойти он нажимает воспламенитель
                """;
        String language = "russian";
        String encrypted = new Vigenere(ResourceHelpers.loadAlphabet(language), password).encrypt(text);

        var breaker = new VigenerCipherBreaker("russian");
        assertEquals(text, breaker.decrypt(encrypted));
    }
}