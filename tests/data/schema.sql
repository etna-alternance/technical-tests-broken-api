DROP TABLE IF EXISTS `product`;

CREATE TABLE `product`
(
    id    int(11)                                                        NOT NULL AUTO_INCREMENT,
    name  varchar(512)                                                   NOT NULL,
    type  enum ('clothing', 'kitchen', 'furniture', 'lighting', 'books') NOT NULL,
    price int(11) UNSIGNED                                               NOT NULL,
    PRIMARY KEY (id)
) ENGINE = InnoDB;
