import express from 'express';
import cors from 'cors';
import http from 'http';
import { Server } from 'socket.io';

const app = express();
const server = http.createServer(app);
const port = process.env.PORT || 5000

const startServer = () =>{
    app.use(cors());
    app.use(express.urlencoded({extended: true}));
    app.use(express.json());

    const io = new Server(server, {
      allowEIO3:true,
        cors: {
          origin: '*',
          methods: ["GET", "POST"],
        },
      });
      
    // Approach 1: class for socket namespace 

    io.on('connection', socket =>{
        console.log(`['USER CONNECTED'] id: ${socket.id}`)


        socket.on('test', (req)  =>{
          socket.broadcast.emit('test', req)
        })

        socket.on('disconnect', () =>{
        console.log(`User is disconnected to ${socket.id}`)

        });
    });
    
    app.get('/', function(req, res){
      res.send("hello world");
    });

    server.listen(port, ()=>{
        console.log(`listening on ${port}`);
    });

}


startServer();