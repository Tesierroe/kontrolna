# kontrolna

Створити програму яка парсить HTML сторінку залежно від параметрів виклику, виклик формату:

python main.py -url www.google.com

Якщо не вказано шлях зробити запит у користувача
Перевірка чи валідна лінка
Знайти всі лінки на сторінці(Перевірити що лінка валідна requests.get (status code == 200))
Посилання у яких статус код 200 зберегти в окремий файл , всі інші у файл з назвою broken_links.txt

- ДОПОВНЕННЯ:

Оформити належним чином репозиторій (всі потрібні файли, опис, requirements.txt ...)
Додати логування де треба (самі для себе визначте критичні місця)
Спробувати розібратися з принципами SOLID і реалізувати їх у ДЗ
Доповнення: 
Програма вміє працювати з pdf файлами виклик формату python main.py --pdf {шлях до файлу} 
якщо шлях не вказано користувачеві пропонують його ввести в консолі Програма шукає всі лінки в PDF файлі,
перевіряє їх на валідність (отримати статус код 200) .
Посилання у яких статус код 200 зберегти в окремий файл ,
всі інші у файл з назвою broken_links.txt


