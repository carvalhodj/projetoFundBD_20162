-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema manutencao
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema manutencao
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `manutencao` DEFAULT CHARACTER SET utf8 ;
USE `manutencao` ;

-- -----------------------------------------------------
-- Table `manutencao`.`Cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `manutencao`.`Cliente` (
  `cpf` VARCHAR(50) NOT NULL,
  `nomeCli` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`cpf`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `manutencao`.`Computador`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `manutencao`.`Computador` (
  `numSerie` VARCHAR(50) NOT NULL,
  `modelo` VARCHAR(50) NOT NULL,
  `cpfCli` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`numSerie`),
  INDEX `fk_Computador_1_idx` (`cpfCli` ASC),
  CONSTRAINT `fk_Computador_1`
    FOREIGN KEY (`cpfCli`)
    REFERENCES `manutencao`.`Cliente` (`cpf`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `manutencao`.`Upgrade_Revisao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `manutencao`.`Upgrade_Revisao` (
  `numSerieComputador` VARCHAR(50) NOT NULL,
  `dataProgramada` VARCHAR(50) NOT NULL,
  `dataUltimoUpgrade` VARCHAR(50) NULL COMMENT '		',
  `dataExecutada` VARCHAR(50) NULL,
  PRIMARY KEY (`numSerieComputador`, `dataProgramada`),
  CONSTRAINT `fk_Upgrade_Revisao_1`
    FOREIGN KEY (`numSerieComputador`)
    REFERENCES `manutencao`.`Computador` (`numSerie`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `manutencao`.`Peca`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `manutencao`.`Peca` (
  `codPeca` VARCHAR(50) NOT NULL,
  `descricao` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`codPeca`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `manutencao`.`Peca_Upgrade_Revisao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `manutencao`.`Peca_Upgrade_Revisao` (
  `numSerieMaquina` VARCHAR(50) NOT NULL,
  `dataProgramadaServico` VARCHAR(50) NOT NULL,
  `codPecaServico` VARCHAR(50) NOT NULL,
  `quantidade` INT NOT NULL,
  PRIMARY KEY (`numSerieMaquina`, `dataProgramadaServico`, `codPecaServico`),
  INDEX `fk_Peca_Upgrade_Revisao_2_idx` (`codPecaServico` ASC),
  CONSTRAINT `fk_Peca_Upgrade_Revisao_1`
    FOREIGN KEY (`numSerieMaquina` , `dataProgramadaServico`)
    REFERENCES `manutencao`.`Upgrade_Revisao` (`numSerieComputador` , `dataProgramada`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Peca_Upgrade_Revisao_2`
    FOREIGN KEY (`codPecaServico`)
    REFERENCES `manutencao`.`Peca` (`codPeca`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;