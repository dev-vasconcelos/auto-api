-- MySQL Script generated by MySQL Workbench
-- sáb 25 set 2021 15:18:28
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`tb_inquilino`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_inquilino` (
  `idtb_inquilino` INT NOT NULL,
  PRIMARY KEY (`idtb_inquilino`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_produto`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_produto` (
  `idtb_produto` INT NOT NULL,
  PRIMARY KEY (`idtb_produto`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_plano`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_plano` (
  `idtb_plano` INT NOT NULL,
  `observacao` VARCHAR(255) NULL,
  `qtd_usuarios` INT NOT NULL DEFAULT 1,
  `qtd_cnpjs` INT NOT NULL DEFAULT 1,
  `qtd_veiculos` INT NOT NULL DEFAULT 1,
  `qtd_horas_desenvolvimento` INT NOT NULL DEFAULT 0,
  `valor_usuario` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `valor_cnpj` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `valor_veiculo` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `valor_hora_desenvolvimento` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `valor_total_modulos` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `desconto` DECIMAL(3,2) NOT NULL DEFAULT 0.0,
  `valor_total` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `periodo` INT NOT NULL DEFAULT mensal COMMENT 'Enum{\n          mensal;\n          trimestral;\n          semestral;\n          anual;\n}\n\n',
  `is_suporte` TINYINT NOT NULL DEFAULT 0,
  `tb_produto_idtb_produto` INT NOT NULL,
  PRIMARY KEY (`idtb_plano`),
  INDEX `fk_tb_plano_tb_produto1_idx` (`tb_produto_idtb_produto` ASC) VISIBLE,
  CONSTRAINT `fk_tb_plano_tb_produto1`
    FOREIGN KEY (`tb_produto_idtb_produto`)
    REFERENCES `mydb`.`tb_produto` (`idtb_produto`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_vendedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_vendedor` (
  `idtb_vendedor` INT NOT NULL,
  PRIMARY KEY (`idtb_vendedor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_contrato`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_contrato` (
  `idtb_contrato` INT NOT NULL,
  `observacao` VARCHAR(255) NULL,
  `data_emissão` DATETIME NOT NULL DEFAULT Data atual,
  `data_aceite` DATETIME NULL,
  `data_inicio` DATETIME NULL,
  `data_final` DATETIME NULL,
  `qtd_meses` INT NOT NULL DEFAULT 12,
  `situação` INT NOT NULL DEFAULT Em_espera COMMENT 'enum{\n         Em_espera;\n         Ativo;\n         Vencido;\n}',
  `tipo_pagamento` INT NULL COMMENT 'enum{\n           Boleto;\n           Transferência;\n           dinheiro;\n}',
  `acrescimo` DECIMAL(3,2) NOT NULL DEFAULT 0.0,
  `desconto` DECIMAL(3,2) NOT NULL DEFAULT 0.0,
  `valor_total` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `tb_inquilino_idtb_inquilino` INT NOT NULL,
  `tb_vendedor_idtb_vendedor` INT NOT NULL,
  PRIMARY KEY (`idtb_contrato`),
  INDEX `fk_tb_contrato_tb_inquilino_idx` (`tb_inquilino_idtb_inquilino` ASC) VISIBLE,
  INDEX `fk_tb_contrato_tb_vendedor1_idx` (`tb_vendedor_idtb_vendedor` ASC) VISIBLE,
  CONSTRAINT `fk_tb_contrato_tb_inquilino`
    FOREIGN KEY (`tb_inquilino_idtb_inquilino`)
    REFERENCES `mydb`.`tb_inquilino` (`idtb_inquilino`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_contrato_tb_vendedor1`
    FOREIGN KEY (`tb_vendedor_idtb_vendedor`)
    REFERENCES `mydb`.`tb_vendedor` (`idtb_vendedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_modulo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_modulo` (
  `idtb_modulo` INT NOT NULL,
  `is_suporte` TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`idtb_modulo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_plano_has_tb_modulo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_plano_has_tb_modulo` (
  `tb_plano_idtb_plano` INT NOT NULL,
  `tb_modulo_idtb_modulo` INT NOT NULL,
  PRIMARY KEY (`tb_plano_idtb_plano`, `tb_modulo_idtb_modulo`),
  INDEX `fk_tb_plano_has_tb_modulo_tb_modulo1_idx` (`tb_modulo_idtb_modulo` ASC) VISIBLE,
  INDEX `fk_tb_plano_has_tb_modulo_tb_plano1_idx` (`tb_plano_idtb_plano` ASC) VISIBLE,
  CONSTRAINT `fk_tb_plano_has_tb_modulo_tb_plano1`
    FOREIGN KEY (`tb_plano_idtb_plano`)
    REFERENCES `mydb`.`tb_plano` (`idtb_plano`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_plano_has_tb_modulo_tb_modulo1`
    FOREIGN KEY (`tb_modulo_idtb_modulo`)
    REFERENCES `mydb`.`tb_modulo` (`idtb_modulo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_config_servidor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_config_servidor` (
  `idtb_config_servidor` INT NOT NULL,
  `hostname` VARCHAR(45) NOT NULL,
  `usuario` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `string_conexao` VARCHAR(45) NULL,
  PRIMARY KEY (`idtb_config_servidor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tb_contrato_has_tb_plano`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tb_contrato_has_tb_plano` (
  `tb_contrato_idtb_contrato` INT NOT NULL,
  `tb_plano_idtb_plano` INT NOT NULL,
  `qtd_adicional_usuario` INT NOT NULL DEFAULT 0,
  `qtd_adicional_cnpj` INT NOT NULL DEFAULT 0,
  `qtd_adicional_veiculo` INT NOT NULL DEFAULT 0,
  `qtd_adicional_horas_desenvolvimento` INT NOT NULL DEFAULT 0,
  `valor_total_usuarios` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `valor_total_cnpj` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `valor_total_veiculo` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `valor_total_horas_desenvolvimento` DECIMAL(6,2) NOT NULL DEFAULT 0.0,
  `data_implantacao` DATETIME NULL,
  `valor_implantacao` DECIMAL(6,2) NULL,
  `forma_pagamento_implantacao` INT NULL COMMENT 'enum{\n           Boleto;\n           Transferência;\n           dinheiro;\n}',
  `descricao_implantacao` VARCHAR(255) NULL,
  `desconto` DECIMAL(3,2) NOT NULL DEFAULT 0.0,
  `acrescimo` DECIMAL(3,2) NOT NULL DEFAULT 0.0,
  `tipo_servidor` INT NULL COMMENT 'enum{\n        Serviço Próprio;\n        Serviço Compartilhado;\n        Apenas Software;\n}',
  `responsavel_infra` INT NULL COMMENT 'enum{\n         TranspNet;\n         Stark;\n         Outro;\n}',
  `qtd_acessos` INT NULL,
  `tipo_treinamento` INT NOT NULL DEFAULT Sem Treinamento COMMENT 'enum{\n         Sem Treinamento = 0;\n         Presencial = 1;\n         Online = 2; \n}',
  `horas_treinamento` INT NOT NULL DEFAULT 0,
  `sub_dominio` VARCHAR(45) NULL,
  `tb_config_servidor_base_dados` INT NOT NULL,
  `tb_config_servidor_windows` INT NOT NULL,
  PRIMARY KEY (`tb_contrato_idtb_contrato`, `tb_plano_idtb_plano`),
  INDEX `fk_tb_contrato_has_tb_plano_tb_plano1_idx` (`tb_plano_idtb_plano` ASC) VISIBLE,
  INDEX `fk_tb_contrato_has_tb_plano_tb_contrato1_idx` (`tb_contrato_idtb_contrato` ASC) VISIBLE,
  INDEX `fk_tb_contrato_has_tb_plano_tb_config_servidor1_idx` (`tb_config_servidor_base_dados` ASC) VISIBLE,
  INDEX `fk_tb_contrato_has_tb_plano_tb_config_servidor2_idx` (`tb_config_servidor_windows` ASC) VISIBLE,
  CONSTRAINT `fk_tb_contrato_has_tb_plano_tb_contrato1`
    FOREIGN KEY (`tb_contrato_idtb_contrato`)
    REFERENCES `mydb`.`tb_contrato` (`idtb_contrato`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_contrato_has_tb_plano_tb_plano1`
    FOREIGN KEY (`tb_plano_idtb_plano`)
    REFERENCES `mydb`.`tb_plano` (`idtb_plano`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_contrato_has_tb_plano_tb_config_servidor1`
    FOREIGN KEY (`tb_config_servidor_base_dados`)
    REFERENCES `mydb`.`tb_config_servidor` (`idtb_config_servidor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tb_contrato_has_tb_plano_tb_config_servidor2`
    FOREIGN KEY (`tb_config_servidor_windows`)
    REFERENCES `mydb`.`tb_config_servidor` (`idtb_config_servidor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`usuairo_contrato`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`usuairo_contrato` (
  `idusuairo_contrato` INT NOT NULL,
  `tb_contrato_idtb_contrato` INT NOT NULL,
  PRIMARY KEY (`idusuairo_contrato`),
  INDEX `fk_usuairo_contrato_tb_contrato1_idx` (`tb_contrato_idtb_contrato` ASC) VISIBLE,
  CONSTRAINT `fk_usuairo_contrato_tb_contrato1`
    FOREIGN KEY (`tb_contrato_idtb_contrato`)
    REFERENCES `mydb`.`tb_contrato` (`idtb_contrato`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
