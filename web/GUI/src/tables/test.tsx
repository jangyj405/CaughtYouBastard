import * as React from 'react'
import {DataGrid, GridColDef, GridValueGetterParams} from '@mui/x-data-grid'


export const columns: GridColDef[] = [
    {field: 'id', headerName: 'ID', width:70},
    {field: 'car_number', headerName: '차량 번호', width: 130},
    {field: 'created_at', headerName: "생성 일자", width: 150}
]

export const rows = (data: string[]) => {

    const arr: any = data.map((data: string, id: number) =>{
        console.log("rows data is ", data)
        return {id, car_number: data}
    })
    console.log('rows arr is ', arr)
    return arr
}
/*
export const rows =  [
    {id: 1, car_number: "24가 3929", created_at: "2023-08"}
]
*/