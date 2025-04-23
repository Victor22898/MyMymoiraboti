document.addEventListener('DOMContentLoaded', function() {
    const translateButton = document.getElementById('translateBtn');
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const sourceLangSelect = document.getElementById('sourceLang');
    const targetLangSelect = document.getElementById('targetLang');

    // Мини-база переводов в обе стороны
    const translations = {
        "привет": "hello",
        "hello": "привет",
        "спасибо": "thank you",
        "thank you": "спасибо",
        "как дела": "how are you",
        "how are you": "как дела",
        "добрый день": "good afternoon",
        "good afternoon": "добрый день",
        "до свидания": "goodbye",
        "goodbye": "до свидания",
        "я люблю тебя": "i love you",
        "i love you": "я люблю тебя"
    };

    translateButton.addEventListener('click', function() {
        const textToTranslate = inputText.value.toLowerCase().trim();
        const sourceLang = sourceLangSelect.value;
        const targetLang = targetLangSelect.value;

        if (textToTranslate === '') {
            outputText.value = 'Пожалуйста, введите текст для перевода.';
            return;
        }

        // Проверяем, есть ли перевод в мини-базе
        if (translations.hasOwnProperty(textToTranslate)) {
            outputText.value = translations[textToTranslate];
            return;
        }

        outputText.value = 'Переводим...';

        fetch('https://translate.astian.org/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                q: textToTranslate,
                source: sourceLang,
                target: targetLang,
                format: 'text'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.translatedText) {
                outputText.value = data.translatedText;
            } else if (data.error) {
                outputText.value = 'Ошибка перевода: ' + data.error;
            } else {
                outputText.value = 'Ошибка перевода.';
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            outputText.value = 'Ошибка перевода. Проверьте подключение к интернету или попробуйте позже.';
        });
    });
});
