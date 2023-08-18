import React from 'react'
import dayjs, {Dayjs} from 'dayjs'
import {car_pass_log_columns as columns, car_pass_log_rows as rows} from '../../tables/attribute'
import {DataGrid} from '@mui/x-data-grid'
import { Button } from '@material-ui/core'


import { DemoContainer, DemoItem } from '@mui/x-date-pickers/internals/demo'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';

// mui search bar
// https://mui.com/material-ui/react-app-bar/

export default function CarNumberLog() 
{
    const [value, setValue] = React.useState<Dayjs | null>(dayjs('2022-04-17'));
    console.log("value is ", value)
    return (
        <React.Fragment>
            <div style={{
                paddingLeft: '300px',
                height: '100%', width:'50%'}}
            >
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <DemoContainer components={['DateCalendar', 'DateCalendar', 'DateCalendar']}>
                     
                        <DateCalendar
                            value={value}
                            defaultValue={dayjs('2022-04-17')}
                            views={['year', 'month', 'day']}
                        />
                    </DemoContainer>
                </LocalizationProvider>
                <div style={{display:'flex', justifyContent:'space-between',  alignItems: 'center'}}>
                <h4 style={{paddingLeft: "50px"}}>차량 로그</h4>
                <form>
                    <input className='Search-box' type="text" placeholder='Search...' name="search" />
                    <Button><i className="fa fa-search"></i></Button>
                </form>            
               

                </div>
            <DataGrid  
                columns={columns}
                rows={rows()}
            />
            </div>
        </React.Fragment>
    )
}