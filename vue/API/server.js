import express from "express";
import cors from "cors";
import db from "./src/db.js"
import models from "./src/models/index.js";
import routes from "./src/routes/index.js";
const { user } = models;
import passport  from "./src/passport.js";
import userSeeder from "./src/seeders/demo-user.seeder.js";

const app = express();

app.set('trust proxy', true);
app.use(cors());

app.use(express.json());
app.use(passport.initialize());

app.use('/api', routes.userRoutes);

db.sync({ force: true })
    .then(() => {
    userSeeder.up(db.queryInterface, db.Sequelize);
    console.log(`Database & tables created!`);
  })
  .catch((err) => { console.log(err) });

  const server = app.listen(3000, '0.0.0.0',() => console.log("Servidor iniciado na porta 3000"));

  process.on('SIGINT', cleanDBAndExit);
  process.on('SIGTERM', cleanDBAndExit);
  
  function cleanDBAndExit() {
    db.drop()
      .then(() => {
        console.log('Database cleaned!');
        server.close(() => {
          console.log('Server stopped');
          process.exit();
        });
      })
      .catch((err) => {
        console.error('Error cleaning database:', err);
        server.close(() => {
          console.log('Server stopped');
          process.exit();
        });
      });
  }