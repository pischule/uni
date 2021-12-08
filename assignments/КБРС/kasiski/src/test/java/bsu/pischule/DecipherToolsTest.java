package bsu.pischule;

import bsu.pischule.ciphers.Vigenere;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

import static bsu.pischule.ResourceHelpers.loadAlphabet;
import static org.junit.jupiter.api.Assertions.assertEquals;

class DecipherToolsTest {
    @Test
    void testSubstrings() {
        assertEquals("bc", "abc".substring(1, 3));
    }

    @ParameterizedTest
    @ValueSource(strings = {"это", "примеры", "паролей", "которыми", "я", "могу", "зашифровать", "текст"})
    void kasiskiAnyCase(String password) {
        String text = """
                Аналогия закона вследствие публичности данных отношений перманентно возмещает аккредитив Договор своевременно исполняет кредитор что не имеет аналогов в англо-саксонской правовой системе Платежный документ в представлениях континентальной школы права возмещает закон
                В зависимости от выбранного способа защиты гражданских прав обязательство неравноправно наследует объект права когда речь идет об ответственности юридического лица Задаток нормативно представляет собой кредитор Норма как следует из теоретических исследований обязывает задаток
                Новация если рассматривать процессы в рамках частно-правовой теории требует взаимозачет именно такой позиции придерживается арбитражная практика В самом общем случае муниципальная собственность законодательно подтверждает платежный документ В ряде недавних судебных решений концессия правомерна Франшиза антиконституционна Безвозмездное изъятие как неоднократно наблюдалось при чрезмерном вмешательстве государства в данные правоотношения несостоятельно
                """;
        Vigenere vigenere = new Vigenere(loadAlphabet("russian"), password);
        String encrypted = vigenere.encrypt(text);
        System.out.println(encrypted);
        assertEquals(password.length(), DecipherTools.findKeyLength(encrypted));
    }
}