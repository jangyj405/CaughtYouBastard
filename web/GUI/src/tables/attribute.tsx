import * as React from 'react'
import {DataGrid, GridColDef, GridValueGetterParams} from '@mui/x-data-grid'


export const car_number_list_columns: GridColDef[] = [
    {field: 'id', headerName: 'ID', width:70},
    {field: 'car_number', headerName: '차량 번호', width: 130},
    {field: 'created_at', headerName: "생성 일자", width: 180}
]

export const car_number_list_rows = (data: string[]) => {

    const arr: any = data.map((data: string, id: number) => {
        console.log("rows data is ", data)
        const date = new Date(data[2]).toJSON().replace("T", " ").substring(0,19)
        return {id : id+1, car_number: data[1], created_at: date}
    })
    console.log('rows arr is ', arr)
    return arr
}

export const car_pass_log_columns: GridColDef[] = [
    {field: 'id', headerName:'ID', width: 70},
    {field: "pi_id", headerName: "카메라 번호", width: 70},
    {field: 'car_number', headerName: '차량 번호', width: 130},
    {
        field: 'image', headerName: '차랑 사진', width: 80,
        renderCell: (parmas) => 
            <img height={80} width={80} src={parmas.value} />
        
    },
    {field: 'time', headerName: "인지 시간", width: 300},
    {field: 'isblock', headerName: "차량 통과 여부", width: 90}
]

export const car_pass_log_rows = (data: string[]) => {

    const arr: any = data.map((data:string, id:number) => {
        console.log("Arr data is", data)
        const date = new Date(data[6]).toJSON().replace("T", " ").substring(0,19)
        return {id: id+1, car_number: data[2],  pi_id: data[1], time: date, image: data[4], isblock: data[5] == "1" ? "True" :"False"}
    })
    return arr
    /*
    {id:data.id, pi_id:2,  car_number:"test2", isblock: false, time: "4567", created_at: "4567",
    image: require("./dog_2.jpeg"),
        //"https://image.shutterstock.com/image-photo/small-juicy-hamburger-canapes-on-260nw-570368917.jpg"
    },
    {id:1, pi_id:2, car_number:"test", isblock: true, time: "1234", created_at: "1234", image:require("./dog_2.jpeg")}
    ]
    */
}
/*
export const rows =  [
    {id: 1, car_number: "24가 3929", created_at: "2023-08"}
]
*/