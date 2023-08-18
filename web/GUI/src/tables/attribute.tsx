import * as React from 'react'
import {DataGrid, GridColDef, GridValueGetterParams} from '@mui/x-data-grid'


export const car_number_list_columns: GridColDef[] = [
    {field: 'id', headerName: 'ID', width:70},
    {field: 'car_number', headerName: '차량 번호', width: 130},
    {field: 'created_at', headerName: "생성 일자", width: 300}
]

export const car_number_list_rows = (data: string[]) => {

    const arr: any = data.map((data: string, id: number) => {
        console.log("rows data is ", data)
        return {id : id+1, car_number: data[1], created_at: data[2]}
    })
    console.log('rows arr is ', arr)
    return arr
}

export const car_pass_log_columns: GridColDef[] = [
    {field: 'id', headerName:'ID', width: 70},
    {field: "pi_id", headerName: "카메라 번호", width: 70},
    {field: 'car_number', headerName: '차량 번호', width: 130},
    {field: 'time', headerName: "인지 시간", width: 150},
    {field: 'isblock', headerName: "차량 통과 여부", width: 70},
    {field: 'created_at', headerName: "생성 일자", width: 150}
]

export const car_pass_log_rows = () => {
    //const arr: any = data.map((data: string) => {
    //})
    return [
    {id:2, pi_id:2, car_number:"test2", isblock: false, time: "4567", created_at: "4567"},
    {id:1, pi_id:2, car_number:"test", isblock: true, time: "1234", created_at: "1234"}
    ]
}
/*
export const rows =  [
    {id: 1, car_number: "24가 3929", created_at: "2023-08"}
]
*/