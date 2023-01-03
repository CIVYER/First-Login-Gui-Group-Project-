drop database if exists project_database;

-- MySQL Workbench Synchronization
-- Generated: 2023-01-03 21:42
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: acer

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `project_database` DEFAULT CHARACTER SET utf8 ;

CREATE TABLE IF NOT EXISTS `project_database`.`Log History` (
  `LHistory_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `Login_ID` INT(11) NOT NULL,
  `Signup_ID` INT(11) NOT NULL,
  `Log_DT` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `Log_Name` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`LHistory_ID`),
  INDEX `fk_Log History_Log in1_idx` (`Login_ID` ASC) VISIBLE,
  INDEX `fk_Log History_Sign up1_idx` (`Signup_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Log History_Log in1`
    FOREIGN KEY (`Login_ID`)
    REFERENCES `project_database`.`Log in` (`Login_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Log History_Sign up1`
    FOREIGN KEY (`Signup_ID`)
    REFERENCES `project_database`.`Sign up` (`Signup_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`User Profile` (
  `User_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `Login_ID` INT(11) NOT NULL,
  `Signup_ID` INT(11) NOT NULL,
  `Account_TypeID` INT(11) NOT NULL,
  `User_lname` CHAR(30) NULL DEFAULT NULL,
  `User_fname` CHAR(30) NULL DEFAULT NULL,
  `User_mname` CHAR(30) NULL DEFAULT NULL,
  `User_dob` VARCHAR(25) NULL DEFAULT NULL,
  `User_gender` CHAR(15) NULL DEFAULT NULL,
  `User_pob` CHAR(255) NULL DEFAULT NULL,
  `User_civilstatus` CHAR(15) NULL DEFAULT NULL,
  `User_nationality` CHAR(50) NULL DEFAULT NULL,
  `User_religion` CHAR(50) NULL DEFAULT NULL,
  `User_mobile` VARCHAR(50) NULL DEFAULT NULL,
  `User_address` VARCHAR(255) NULL DEFAULT NULL,
  `User_municipality_region` CHAR(50) NULL DEFAULT NULL,
  `User_city` CHAR(50) NULL DEFAULT NULL,
  `User_barangay` CHAR(50) NULL DEFAULT NULL,
  `User_zipcode` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`User_ID`),
  INDEX `fk_User Profile_Log in1_idx` (`Login_ID` ASC) VISIBLE,
  INDEX `fk_User Profile_Sign up1_idx` (`Signup_ID` ASC) VISIBLE,
  INDEX `fk_User Profile_Account_Type1_idx` (`Account_TypeID` ASC) VISIBLE,
  CONSTRAINT `fk_User Profile_Log in1`
    FOREIGN KEY (`Login_ID`)
    REFERENCES `project_database`.`Log in` (`Login_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User Profile_Sign up1`
    FOREIGN KEY (`Signup_ID`)
    REFERENCES `project_database`.`Sign up` (`Signup_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_User Profile_Account_Type1`
    FOREIGN KEY (`Account_TypeID`)
    REFERENCES `project_database`.`Account_Type` (`Account_TypeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`Sign up` (
  `Signup_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `Verification_ID` INT(11) NOT NULL,
  `Login_ID` INT(11) NOT NULL,
  `Email` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`Signup_ID`),
  INDEX `fk_Sign up_Verification1_idx` (`Verification_ID` ASC) VISIBLE,
  INDEX `fk_Sign up_Log in1_idx` (`Login_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Sign up_Verification1`
    FOREIGN KEY (`Verification_ID`)
    REFERENCES `project_database`.`Verification` (`Verification_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Sign up_Log in1`
    FOREIGN KEY (`Login_ID`)
    REFERENCES `project_database`.`Log in` (`Login_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`user` (
  `username` VARCHAR(16) NOT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `password` VARCHAR(32) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`Verification` (
  `Verification_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `Verification_code` VARCHAR(50) NULL DEFAULT NULL,
  PRIMARY KEY (`Verification_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`Forgot Password` (
  `FPass_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `User_ID` INT(11) NOT NULL,
  `Login_ID` INT(11) NOT NULL,
  `Verification_ID` INT(11) NOT NULL,
  PRIMARY KEY (`FPass_ID`),
  INDEX `fk_Forgot Password_User Profile1_idx` (`User_ID` ASC) VISIBLE,
  INDEX `fk_Forgot Password_Log in1_idx` (`Login_ID` ASC) VISIBLE,
  INDEX `fk_Forgot Password_Verification1_idx` (`Verification_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Forgot Password_User Profile1`
    FOREIGN KEY (`User_ID`)
    REFERENCES `project_database`.`User Profile` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Forgot Password_Log in1`
    FOREIGN KEY (`Login_ID`)
    REFERENCES `project_database`.`Log in` (`Login_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Forgot Password_Verification1`
    FOREIGN KEY (`Verification_ID`)
    REFERENCES `project_database`.`Verification` (`Verification_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`Log in` (
  `Login_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `Login_password` VARCHAR(45) NULL DEFAULT NULL,
  `Login_Username` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`Login_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`Account_Type` (
  `Account_TypeID` INT(11) NOT NULL AUTO_INCREMENT,
  `AccountType` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`Account_TypeID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`login_state` (
  `login_stateID` INT(11) NOT NULL AUTO_INCREMENT,
  `Login_ID` INT(11) NOT NULL,
  `Logged_in` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`login_stateID`),
  INDEX `fk_login_state_Log in1_idx` (`Login_ID` ASC) VISIBLE,
  CONSTRAINT `fk_login_state_Log in1`
    FOREIGN KEY (`Login_ID`)
    REFERENCES `project_database`.`Log in` (`Login_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

CREATE TABLE IF NOT EXISTS `project_database`.`P_Backup` (
  `P_Backup_ID` INT(11) NOT NULL AUTO_INCREMENT,
  `User_ID` INT(11) NOT NULL,
  `User_lname` CHAR(30) NULL DEFAULT NULL,
  `User_fname` CHAR(30) NULL DEFAULT NULL,
  `User_mname` CHAR(30) NULL DEFAULT NULL,
  `User_dob` VARCHAR(25) NULL DEFAULT NULL,
  `User_gender` CHAR(15) NULL DEFAULT NULL,
  `User_pob` CHAR(255) NULL DEFAULT NULL,
  `User_civilstatus` CHAR(15) NULL DEFAULT NULL,
  `User_nationality` CHAR(50) NULL DEFAULT NULL,
  `User_religion` CHAR(50) NULL DEFAULT NULL,
  `User_mobile` VARCHAR(50) NULL DEFAULT NULL,
  `User_address` VARCHAR(255) NULL DEFAULT NULL,
  `User_municipality_region` CHAR(50) NULL DEFAULT NULL,
  `User_city` CHAR(50) NULL DEFAULT NULL,
  `User_barangay` CHAR(50) NULL DEFAULT NULL,
  `User_zipcode` VARCHAR(50) NULL DEFAULT NULL,
  `b_date` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`P_Backup_ID`),
  INDEX `fk_User Profile_copy1_User Profile1_idx` (`User_ID` ASC) VISIBLE,
  CONSTRAINT `fk_User Profile_copy1_User Profile1`
    FOREIGN KEY (`User_ID`)
    REFERENCES `project_database`.`User Profile` (`User_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
