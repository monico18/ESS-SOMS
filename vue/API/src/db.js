import { Sequelize } from "sequelize";

const dbStorage = "./db.sqlite";

const sequelize = new Sequelize({
    dialect: "sqlite",
    storage:dbStorage,
});

export default sequelize;