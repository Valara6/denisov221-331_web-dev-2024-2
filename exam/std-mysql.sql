-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: std-mysql
-- Время создания: Июн 13 2024 г., 14:14
-- Версия сервера: 5.7.26-0ubuntu0.16.04.1
-- Версия PHP: 8.1.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `std_2484_exam`
--
CREATE DATABASE IF NOT EXISTS `std_2484_exam` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `std_2484_exam`;

-- --------------------------------------------------------

--
-- Структура таблицы `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `year` year(4) NOT NULL,
  `publisher` varchar(50) NOT NULL,
  `author` varchar(50) NOT NULL,
  `pages` int(11) NOT NULL,
  `cover` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `books`
--

INSERT INTO `books` (`id`, `name`, `description`, `year`, `publisher`, `author`, `pages`, `cover`) VALUES
(48, 'Маленький Принц', 'Книга** \"Маленький принц\"** Антуана де Сент-Экзюпери впервые вышла в 1944 году и с тех пор завоевала сердца читателей во всём мире. Книга-притча, философская сказка о маленьком **мальчике**, который путешествовал по разным планетам и в конце оказался на нашей Земле. Главные герои - сам принц, его *друг лётчик*, красавица-роза, мудрый Лис - расскажут читателям об ответственности за тех, кого приручили, о жизни и о великой любви и дружбе! В книге классический перевод **Норы Галь **и трогательные иллюстрации самого автора.\r\n', '2000', 'Классика', 'Экзюпери', 200, 24),
(49, 'Тихий Дон', 'Эпопея о **донском казачестве** в годы Первой мировой и Гражданской войны. В центре сюжета — **Григорий Мелехов**: его роман с замужней соседкой Аксиньей, подневольная женитьба на другой, бегство с родного хутора. Григорий воюет, ищет истину, мечется между красными и белыми, женой и возлюбленной, теряет всех своих близких — и в финале оказывается в полном одиночестве с маленьким сыном на руках. Роман, претендующий на статус советских «Войны и мира», — редкая для **подцензурной литературы** панорама Гражданской войны, увиденной с разных точек зрения.', '1991', 'Классика', 'Михаил Шолохов', 1000, 25),
(50, 'Граф Монте-Кристо', 'Граф Монте-Кристо\", один из самых популярных романов Александра Дюма, имеет ошеломительный успех у читателей. Его сюжет автор почерпнул из архивов парижской полиции. Подлинная жизнь сапожника **Франсуа Пико**, ставшего прототипом **Эдмона Дантеса**, под пером настоящего художника превратилась в захватывающую книгу о мученике замка Иф и о парижском ангеле мщения.\n', '1995', 'Классика', 'Александр Дюма', 400, 26);

-- --------------------------------------------------------

--
-- Структура таблицы `book_cover`
--

CREATE TABLE `book_cover` (
  `id` int(11) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `mime_type` varchar(255) DEFAULT NULL,
  `hash` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `book_cover`
--

INSERT INTO `book_cover` (`id`, `filename`, `mime_type`, `hash`) VALUES
(24, 'mp.jpg', 'image/jpeg', '062d221fcda7f8f725bbf5485e57e50a'),
(25, 'td.jpg', 'image/jpeg', 'b9e2bf1bb138b5f3bd12dcbb1d05ee6a'),
(26, 'gmk.jpg', 'image/jpeg', '190d4aa50b4dded136c1dc893705ccf9');

-- --------------------------------------------------------

--
-- Структура таблицы `genres`
--

CREATE TABLE `genres` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `genres`
--

INSERT INTO `genres` (`id`, `name`) VALUES
(1, 'Детектив'),
(2, 'Роман'),
(3, 'Приключения'),
(4, 'Фентези'),
(5, 'Боевик');

-- --------------------------------------------------------

--
-- Структура таблицы `m2m_books_genres`
--

CREATE TABLE `m2m_books_genres` (
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `m2m_books_genres`
--

INSERT INTO `m2m_books_genres` (`book_id`, `genre_id`) VALUES
(49, 2),
(50, 2),
(50, 3),
(48, 3);

-- --------------------------------------------------------

--
-- Структура таблицы `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `book` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `review_status` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `reviews`
--

INSERT INTO `reviews` (`id`, `book`, `user`, `rating`, `text`, `date`, `review_status`) VALUES
(9, 50, 1, 5, 'хорошая книга', '2024-06-13 12:01:39', 2),
(10, 50, 3, 0, 'Не читал', '2024-06-13 12:10:36', 2),
(11, 50, 2, 3, 'Хорошо', '2024-06-13 12:10:39', 2),
(12, 50, 8, 1, 'Не понравилось', '2024-06-13 12:40:14', 2),
(13, 50, 9, 5, 'sdf', '2024-06-13 12:40:44', 1),
(14, 50, 11, 5, 'Ок', '2024-06-13 12:47:03', 1),
(15, 50, 12, 0, 'Не ок', '2024-06-13 12:47:33', 1),
(16, 50, 16, 4, 'Читал', '2024-06-13 13:30:02', 1);

-- --------------------------------------------------------

--
-- Структура таблицы `reviews_status`
--

CREATE TABLE `reviews_status` (
  `id` int(11) NOT NULL,
  `status` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `reviews_status`
--

INSERT INTO `reviews_status` (`id`, `status`) VALUES
(1, 'На рассмотрении'),
(2, 'Одобрена'),
(3, 'Отклонена');

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `name`, `description`) VALUES
(1, 'admin', 'Администратор системы'),
(2, 'moderator', ''),
(3, 'user', '');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `second_name` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `role` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `login`, `password_hash`, `second_name`, `first_name`, `last_name`, `role`) VALUES
(1, 'admin', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Иванов1', 'Иван1', 'Иванович1', 1),
(2, 'mod', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Иванов2', 'Иван2', 'Иванович2', 2),
(3, 'user', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Иванов3', 'Иван3', 'Иванович3', 3),
(7, 'admin1', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Иванов', 'Иван', 'Иванович', 1),
(8, 'user2', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(9, 'user3', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(10, 'user4', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(11, 'user5', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(12, 'user6', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(13, 'user7', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(14, 'user8', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(15, 'user9', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3),
(16, 'user10', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'd', 'd', 'd', 3);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `books_ibfk_1` (`cover`);

--
-- Индексы таблицы `book_cover`
--
ALTER TABLE `book_cover`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `genres`
--
ALTER TABLE `genres`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `m2m_books_genres`
--
ALTER TABLE `m2m_books_genres`
  ADD KEY `book_id` (`book_id`),
  ADD KEY `genre_id` (`genre_id`);

--
-- Индексы таблицы `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book` (`book`),
  ADD KEY `review_status` (`review_status`),
  ADD KEY `user` (`user`);

--
-- Индексы таблицы `reviews_status`
--
ALTER TABLE `reviews_status`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD KEY `role` (`role`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT для таблицы `book_cover`
--
ALTER TABLE `book_cover`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT для таблицы `genres`
--
ALTER TABLE `genres`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT для таблицы `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT для таблицы `reviews_status`
--
ALTER TABLE `reviews_status`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`cover`) REFERENCES `book_cover` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `m2m_books_genres`
--
ALTER TABLE `m2m_books_genres`
  ADD CONSTRAINT `m2m_books_genres_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `m2m_books_genres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`book`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`review_status`) REFERENCES `reviews_status` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reviews_ibfk_3` FOREIGN KEY (`user`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `roles` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
