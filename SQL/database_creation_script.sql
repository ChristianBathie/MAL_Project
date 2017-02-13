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
  `releaseDate` DATE NOT NULL DEFAULT '1900-01-01',
  `englishTitle` VARCHAR(150) NULL,
  `synonymsTitle` VARCHAR(450) NULL,
  `url` VARCHAR(160) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`title` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`Studio`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Studio` (
  `id` INT NOT NULL COMMENT 'Same as MAL DB ID',
  `name` VARCHAR(60) NOT NULL,
  `url` VARCHAR(100) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
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
  `name` VARCHAR(60) NOT NULL,
  `birthday` DATE NOT NULL DEFAULT '1900-01-01',
  `url` VARCHAR(120) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`Staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Staff` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idAnime` INT NOT NULL,
  `idPerson` INT NOT NULL,
  `position` VARCHAR(60) NOT NULL DEFAULT 'Position Unknown',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `Anime_id_idx` (`idAnime` ASC),
  INDEX `Person_id_idx` (`idPerson` ASC),
  CONSTRAINT `idAnime_Staff`
    FOREIGN KEY (`idAnime`)
    REFERENCES `mal_project`.`Anime` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `idPerson_Staff`
    FOREIGN KEY (`idPerson`)
    REFERENCES `mal_project`.`Person` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mal_project`.`Character`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mal_project`.`Character` (
  `id` INT NOT NULL,
  `idAnime` INT NOT NULL,
  `name` VARCHAR(60) NOT NULL,
  `role` VARCHAR(30) NULL COMMENT 'eg Main or Supporting',
  `url` VARCHAR(120) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `idAnime_Character_idx` (`idAnime` ASC),
  CONSTRAINT `idAnime_Character`
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
  `idCharacter` INT NOT NULL,
  `language` VARCHAR(20) NOT NULL DEFAULT 'Japanese',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  INDEX `idStaff_idx` (`idPerson` ASC),
  INDEX `idCharacter_idx` (`idCharacter` ASC),
  CONSTRAINT `idPerson_VoiceRole`
    FOREIGN KEY (`idPerson`)
    REFERENCES `mal_project`.`Person` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `idCharacter_VoiceRole`
    FOREIGN KEY (`idCharacter`)
    REFERENCES `mal_project`.`Character` (`id`)
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
INSERT INTO `mal_project`.`Anime` (`id`, `title`, `releaseDate`, `englishTitle`, `synonymsTitle`, `url`) VALUES (9253, 'Steins;Gate', '2011-04-06', 'Steins;Gate', 'シュタゲ', '/anime/9253/Steins_Gate');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`Person`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`Person` (`id`, `name`, `birthday`, `url`) VALUES (1602, 'John Michael Tatum', '1976-05-25', '/people/1602/John_Michael_Tatum');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`Character`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`Character` (`id`, `idAnime`, `name`, `role`, `url`) VALUES (35252, 9253, 'Rintarou Okabe', 'Main', '/character/35252/Rintarou_Okabe');

COMMIT;


-- -----------------------------------------------------
-- Data for table `mal_project`.`VoiceRole`
-- -----------------------------------------------------
START TRANSACTION;
USE `mal_project`;
INSERT INTO `mal_project`.`VoiceRole` (`id`, `idPerson`, `idCharacter`, `language`) VALUES (DEFAULT, 1602, 35252, 'English');

COMMIT;

