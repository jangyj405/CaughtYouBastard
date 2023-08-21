import React, {useState, useEffect} from 'react'
import Typography from '@mui/material/Typography'
import Dialog from '@mui/material/Dialog'
import Button from '@mui/material/Button'
import { DialogTitle } from '@material-ui/core';
import {DataGrid, GridRowSelectionModel} from '@mui/x-data-grid'
import {car_number_list_columns as columns, car_number_list_rows as rows} from '../../tables/attribute'

import axios from 'axios'

const instance = axios.create({
    baseURL:'http://10.10.14.2:4000',
    timeout: 2000.
})

export interface SimpleDialogProps {
    open: boolean;
    selectedValue: string;
    onClose:(value: string) => void;
};

let car_num: string;

function SimpleDialog(props: SimpleDialogProps) {
    const {onClose, selectedValue, open} = props;

    const handleClose = () => {
        onClose(selectedValue);
    }

    const handleChange = (e: any) =>{
        console.log("e value is ", e.target.value)
        car_num = e.target.value;
    }

    const handleListItemClick = (value: string) =>{
        onClose(value);
    }

    const handelSumit = async (e:any) => {
        const portalDiv = document.getElementById('car_number')!;

        console.log("e:", e.target) 
        const formData = new FormData();
        formData.append("car_num", car_num)
        console.log('portalDiv', portalDiv)
        await instance.post('/car-number/regist', formData)

    }

    return (
        <Dialog onClose={handleClose} open={open}>
            <DialogTitle>새로 등록할 차량 번호를 입력하세요</DialogTitle>
            <form>
                <input 
                    placeholder='ex) 4462'
                    id='car_number'
                    onChange={handleChange}
                />
                <Button onClick={handelSumit}>등록</Button>
            </form>
        </Dialog>
    )
}

export default function MngCarnNum() {
    const [arr, setArr] = useState([]);
    const [open, setOpen] = useState(false);
    const [selectedValue, setSelectedValue] = useState("");
    const handleClose = (value: string) => {
        setOpen(false);
        setSelectedValue(value);
        //fetchData();
    };

    const handleClickOpen = () =>{
        setOpen(true)
    }
    
    useEffect(() => {
        fetchData()
    }, [,setArr])
    
   
   const fetchData = async () => {
        await instance('/car-number').then(response => {
        console.log('response : ', JSON.stringify(response, null, 2))
        setArr(response.data)
       }).catch(error =>{
        console.log('failed', error)
       })
   }

   const [rowSelectionModel, setRowSelectionModel] =
   React.useState<any>([]);

   const [testData, setTestData] =
   React.useState<any>([]);

   let deleteArrtestArr:any[] = []
    const [deleteArr, setDeleteArr] = React.useState<any>([]);
    const handleDeleteButton = async () =>
    {
        console.log("handleDeleteButton is ", rowSelectionModel)
        console.log("test is ", rowSelectionModel.findIndex((test:any,idx: number) => {
            console.log("test value is ", test, idx, test[idx])
            console.log("bolean value is ", test[idx] == idx)
            console.log("arr[test-1] is ", arr[test-1])
            deleteArr.push(arr[test-1][0])
        }))
        console.log("deleteArr2 is ", deleteArr)
        await instance.post('/car-number/delete', deleteArr)
        setDeleteArr([])
    }

    //console.log("arr is ", arr[0][0])
    return (
        <React.Fragment>
            <form>
                {arr.length !=0 ? 
                    <div style={{
                        paddingLeft: '300px',
                        height: '100%', width:'50%'}}>
                        <div className='Car-number-list-head'>
                            <h3 >등록된 차량번호</h3>
                            <div>
                                <Button variant='outlined' onClick={handleClickOpen}>
                                    추가
                                </Button>
                                <Button variant='outlined' onClick={handleDeleteButton}>
                                    삭제
                                </Button>
                            </div>
                    </div>
                <SimpleDialog 
                    selectedValue={selectedValue}
                    open={open}
                    onClose={handleClose}
                />
                        <DataGrid 
                            checkboxSelection
                            disableRowSelectionOnClick
                            onRowSelectionModelChange={(newRowSelectionModel) => {
                                setRowSelectionModel(newRowSelectionModel);
                              }}

                            rows={rows(arr)}
                            columns={columns}
                            /*
                            initialState={{
                                pagination:{
                                    paginationModel:{page:0, pageSize: 20}
                                }
                            }}
                            */
                        />
                    </div>
                    
                : <h4>loading...</h4>}
            </form>
        </React.Fragment>
    )
};