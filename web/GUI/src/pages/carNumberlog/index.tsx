import React, { useEffect } from 'react'
import axios from 'axios'
import {car_pass_log_columns as columns, car_pass_log_rows as rows} from '../../tables/attribute'
import {DataGrid} from '@mui/x-data-grid'
import { Button } from '@material-ui/core'

// mui search bar
// https://mui.com/material-ui/react-app-bar/

const instance = axios.create({
    //baseURL:'http://10.10.14.2:4000',
    baseURL:'http://10.10.14.220:8000',
    timeout: 2000.
})

export default function CarNumberLog() 
{
    const [arr, setArr] = React.useState([]);

    const fetchData = async () => {
        await instance('/car-pass-log').then(response => {
        console.log('response : ', JSON.stringify(response, null, 2))
        setArr(response.data)
       }).catch(error =>{
        console.log('failed', error)
       })
   }

    useEffect(() => {
        let polling = setInterval(() =>{
            fetchData()
        }, 6000)

        return () =>{
            clearInterval(polling)
        }
    }, [])
    
    return (
        <React.Fragment>
            <div style={{
                paddingLeft: '100px', maxWidth: '820px',
                height: '100%', width:'100%'}}
            >
                <div style={{display:'flex', maxWidth: '810px', justifyContent:'space-between',  alignItems: 'center'}}>
                    <h3 style={{paddingLeft: "50px"}}>차량 로그</h3>
                    <form>
                        <input className='Search-box' type="text" placeholder='Search...' name="search" />
                        <Button><i className="fa fa-search"></i></Button>
                    </form>            
            
                </div>
                <DataGrid
                    rowHeight={80}
                    columns={columns}
                    rows={rows(arr)}
                />
            </div>
        </React.Fragment>
    )
}