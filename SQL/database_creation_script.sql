-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mal_project
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mal_project` ;

-- -----------------------------------------------------
-- Schema mal_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mal_project` DEFAULT CHARACTER SET utf8 ;
USE `mal_project` ;

-- -----------------------------------------------------
-- Table `mal_project`.`Anime`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Anime` (
  `id` INT NOT NULL COMMENT 'Same as MAL DB ID',
  `title` VARCHAR(150) NOT NULL,
  `releaseDate` DATE NULL DEFAULT '1900-01-01',
  `titleEnglish` VARCHAR(150) NULL,
  `titleSynonyms` VARCHAR(450) NULL,
  `memberCount` INT NULL,
  `scoreValue` DECIMAL(3,2) NULL,
  `scoreCount` INT NULL,
  `favouriteCount` INT NULL,
  `url` VARCHAR(160) NULL,
  `image` VARCHAR(20) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `url_UNIQUE` (`url` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`Studio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Studio` (
  `id` INT NOT NULL COMMENT 'Same as MAL DB ID',
  `studioName` VARCHAR(60) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`AnimeStudio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`AnimeStudio` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idAnime` INT NOT NULL,
  `idStudio` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `Anime_id_idx` (`idAnime` ASC),
  INDEX `Studio_id_idx` (`idStudio` ASC),
  CONSTRAINT `idAnime_AnimeStudio`
    FOREIGN KEY (`idAnime`)
    REFERENCES `mal_project`.`Anime` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `idStudio_AnimeStudio`
    FOREIGN KEY (`idStudio`)
    REFERENCES `mal_project`.`Studio` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`Person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Person` (
  `id` INT NOT NULL,
  `fullname` VARCHAR(60) NOT NULL,
  `birthday` DATE NULL,
  `favouriteCount` INT NULL,
  `image` VARCHAR(20) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`AnimeStaff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`AnimeStaff` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idAnime` INT NOT NULL,
  `position` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `idAnime_Position_idx` (`idAnime` ASC),
  CONSTRAINT `idAnime_Position`
    FOREIGN KEY (`idAnime`)
    REFERENCES `mal_project`.`Anime` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`Staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Staff` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idPerson` INT NOT NULL,
  `idAnimeStaff` INT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `Person_id_idx` (`idPerson` ASC),
  INDEX `idPosition_Staff_idx` (`idAnimeStaff` ASC),
  CONSTRAINT `idPosition_Staff`
    FOREIGN KEY (`idAnimeStaff`)
    REFERENCES `mal_project`.`AnimeStaff` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `idPerson_Staff`
    FOREIGN KEY (`idPerson`)
    REFERENCES `mal_project`.`Person` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`CharacterProfile`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`CharacterProfile` (
  `id` INT NOT NULL COMMENT 'Same as MAL DB ID',
  `fullname` VARCHAR(60) NOT NULL,
  `favouriteCount` INT NULL,
  `image` VARCHAR(20) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`AnimeCharacter`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`AnimeCharacter` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idAnime` INT NOT NULL,
  `idCharacter` INT NOT NULL,
  `main` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `idCharacter_CharacterAnime_idx` (`idCharacter` ASC),
  INDEX `idAnime_CharacterAnime_idx` (`idAnime` ASC),
  CONSTRAINT `idCharacter_CharacterAnime`
    FOREIGN KEY (`idCharacter`)
    REFERENCES `mal_project`.`CharacterProfile` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `idAnime_CharacterAnime`
    FOREIGN KEY (`idAnime`)
    REFERENCES `mal_project`.`Anime` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`VoiceRole`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`VoiceRole` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idPerson` INT NOT NULL,
  `idAnimeCharacter` INT NOT NULL,
  `language` VARCHAR(20) NOT NULL DEFAULT 'Japanese',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `idStaff_idx` (`idPerson` ASC),
  INDEX `idCharacterAnime_VoiceRole_idx` (`idAnimeCharacter` ASC),
  CONSTRAINT `idPerson_VoiceRole`
    FOREIGN KEY (`idPerson`)
    REFERENCES `mal_project`.`Person` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `idCharacterAnime_VoiceRole`
    FOREIGN KEY (`idAnimeCharacter`)
    REFERENCES `mal_project`.`AnimeCharacter` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`Genre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Genre` (
  `id` INT NOT NULL COMMENT 'Same as MAL DB ID',
  `title` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`AnimeGenre`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`AnimeGenre` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idAnime` INT NOT NULL,
  `idGenre` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `idAnime_AnimeGenre_idx` (`idAnime` ASC),
  INDEX `idGenre_AnimeGenre_idx` (`idGenre` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `idAnime_AnimeGenre`
    FOREIGN KEY (`idAnime`)
    REFERENCES `mal_project`.`Anime` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `idGenre_AnimeGenre`
    FOREIGN KEY (`idGenre`)
    REFERENCES `mal_project`.`Genre` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `mal_project`.`Anime`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`Anime` (`id`, `title`, `releaseDate`, `titleEnglish`, `titleSynonyms`, `memberCount`, `scoreValue`, `scoreCount`, `favouriteCount`, `url`, `image`) VALUES (9253, 'Steins;Gate', '2011-04-06', 'Steins;Gate', 'シュタゲ', 718217, 9.16, 411648, 71013, NULL, NULL);

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`Studio`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`Studio` (`id`, `studioName`) VALUES (1, 'Studio Pierrot');
INSERT INTO `mal_project`.`Studio` (`id`, `studioName`) VALUES (314, 'White Fox');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`AnimeStudio`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`AnimeStudio` (`id`, `idAnime`, `idStudio`) VALUES (1, 9253, 314);

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`Person`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`Person` (`id`, `fullname`, `birthday`, `favouriteCount`, `image`) VALUES (1602, 'John Michael Tatum', '1976-05-25', NULL, NULL);
INSERT INTO `mal_project`.`Person` (`id`, `fullname`, `birthday`, `favouriteCount`, `image`) VALUES (16915, 'Gaku Iwasa', '1974-02-05', NULL, NULL);

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`AnimeStaff`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`AnimeStaff` (`id`, `idAnime`, `position`) VALUES (1, 9253, 'Producer');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`Staff`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`Staff` (`id`, `idPerson`, `idAnimeStaff`) VALUES (DEFAULT, 16915, 1);

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`CharacterProfile`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`CharacterProfile` (`id`, `fullname`, `favouriteCount`, `image`) VALUES (35252, 'Rintarou Okabe', 30207, NULL);

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`AnimeCharacter`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`AnimeCharacter` (`id`, `idAnime`, `idCharacter`, `main`) VALUES (1, 9253, 35252, true);

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`VoiceRole`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`VoiceRole` (`id`, `idPerson`, `idAnimeCharacter`, `language`) VALUES (DEFAULT, 1602, 1, 'English');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`Genre`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`Genre` (`id`, `title`) VALUES (1, 'Action');
INSERT INTO `mal_project`.`Genre` (`id`, `title`) VALUES (24, 'Sci-Fi');
INSERT INTO `mal_project`.`Genre` (`id`, `title`) VALUES (41, 'Thriller');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`AnimeGenre`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`AnimeGenre` (`id`, `idAnime`, `idGenre`) VALUES (DEFAULT, 9253, 24);
INSERT INTO `mal_project`.`AnimeGenre` (`id`, `idAnime`, `idGenre`) VALUES (DEFAULT, 9253, 41);

COMMIT;

