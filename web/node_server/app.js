const express = require("express");

const app = express();
const cors = require('cors');
const multer = require("multer");
const path = require("path");

app.use(cors());
app.use("/static", express.static(path.join(__dirname, "static")));

const port = 4000;

const storage = multer.diskStorage({
    destination: function(req, file, cb) 
    {
        cb(null, 'uploads/')
    },
    filename:function (req, file, cb)
    {
        console.log("file is ", file)
        cb(null, file.originalname + '-'+ Date.now())
    }
});

const uploads = multer({storage})

app.get('/', (req, res) =>{
    res.send('Hello World!');
});

app.post('/file', uploads.single('profile_img'), (req, res,next) =>{
    res.send('Hello World!');
})

app.listen(port, () => {
    console.log('서버가 실행됩니다. ')
})