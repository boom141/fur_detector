import express from 'express';
import fileUpload from 'express-fileupload';
import cors from 'cors';
import http from 'http';
import { Server } from 'socket.io';

const app = express();
const server = http.createServer(app);
const port = process.env.PORT || 5000

const authenticated_devices = []


const startServer = () =>{
    app.use(cors());
    app.use(fileUpload());
    app.use(express.urlencoded({extended: true}));
    app.use(express.json());

    const io = new Server(server, {
      allowEIO3:true,
        cors: {
          origin: '*',
          methods: ["GET", "POST"],
        },
      }); 
      
    io.on('connection', socket =>{
        console.log(`[USER CONNECTED] id: ${socket.id}`)

        socket.on('authenticate_device', (req) =>{
          if(req.access_token){
            authenticated_devices.push(req)
            console.log(authenticated_devices)
          }
        })

        socket.on('manual_control', (req)  =>{
          const mime_type = 'data:image/jpg;base64,';
          const image_src = mime_type + req.file;

          socket.broadcast.emit('manual_control', {frame_src: image_src});
        })

        socket.on('requestControl', data =>{
          socket.broadcast.emit('scannerController', data);
        })


        socket.on('disconnect', () =>{
            console.log(`[USER DISCONNECTED] id: ${socket.id}`)
        });
    });
    
    app.get('/', function(req, res){
      res.send("hello world");
    });
    app.post('/test', function(req, res){
      res.send({data: 'recieved'});
    });

    server.listen(port, ()=>{
        console.log(`listening on ${port}`);
    });

}


startServer();