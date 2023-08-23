import React from 'react';
import styled from 'styled-components'
import {Button} from '@material-ui/core'

import axios from 'axios'

const instance = axios.create({
  //baseURL:'http://10.10.14.2:4000',
  baseURL:'http://10.10.14.220:8000',
    timeout: 2000,
})

const uploadBar = styled.div`
    background-color: #282c34;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
`
 
export default function UploadImg() {
    const fileInput = React.useRef(null);

    const formData = new FormData()

    const handleButtonClick = async e => {
        console.log("hBC prev fileInput is ", fileInput)
        fileInput.current.click();
        console.log("hBC after fileInput is ", fileInput)
    };

    const handleSumitClick = async e => {
        console.log("2. formData is", formData);
        await instance.post('/file', formData).then(response => {
            console.log('response : ', JSON.stringify(response, null, 2))
        }).catch( error => {
            console.log('failed', error)
        })
    }
    
    
    const handleChange = e => {
        console.log("hC prev fileInput is ", fileInput)
        console.log(" e.target.files[0] is", e.target.files[0]);
        formData.append('image', e.target.files[0]);
        renderFile(e.target.files[0]);
        //formData.append("1", "test")
        console.log(" formData is", formData);
    };
    function renderFile(file) {
        let fileDOM = document.createElement("div");
        fileDOM.className = "file";
        fileDOM.innerHTML = `
          <div class="thumbnail">
            <img src="https://img.icons8.com/pastel-glyph/2x/image-file.png" alt="파일타입 이미지" class="image">
          </div>
          <div class="details">
            <header class="header">
              <span class="name">${file.name}</span>
              <span class="size">${file.size}</span>
            </header>
            <div class="progress">
              <div class="bar"></div>
            </div>
            <div class="status">
              <span class="percent">100% done</span>
              <span class="speed">90KB/sec</span>
            </div>
          </div>
        `;
        return fileDOM;
      }

      
    return (
      <React.Fragment>
        <uploadBar>
        <form>
        <div id="files" class="files">
            <div class="file">
                <div class="thumbnail">
                </div>
                <div class="details">
                <header class="header">
                    <span class="name">Photo.png</span>
                    <span class="size">7.5 mb</span>
                </header>
                <div class="progress">
                    <div class="bar"></div>
                </div>
                <div class="status">
                    <span class="percent">37% done</span>
                    <span class="speed">90KB/sec</span>
                </div>
                </div>
            </div>
        </div>
            <Button onClick={handleButtonClick}>파일 업로드</Button>
            <input type="file"
                ref={fileInput}
                multiple="multiple"
                onChange={handleChange}
                style={{ display: "none" }} />
                
            <input onClick={handleSumitClick} type="button" value="업로드"></input>
        </form>
        </uploadBar>
      </React.Fragment>
    );

    /*
    return <MuiThemeProvider theme={theme}>
            <div>
                <h1>test</h1>
                <Button variant="contained" color='primary'>Hello</Button>
            </div>
        </MuiThemeProvider>
     */   
}