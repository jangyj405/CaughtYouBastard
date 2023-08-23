import React from 'react';
import styled from 'styled-components';
import { Link } from 'react-router-dom';

import { Navigation } from 'react-minimal-side-navigation';

import {Sidebar, Menu, MenuItem} from 'react-pro-sidebar'
import Toolbar from '@mui/material/Toolbar';
const Bar = styled.div`
  position: sticky;
  top: 20px;
  width: 10.5rem;
  height: 100%;
  /* position: fixed;
  left: 19rem;
  top: 12rem;
  transform: translate(1em, 12rem); */
`;
//react-pro-sidebar with Mui - https://blog.openreplay.com/simple-sidebars-with-react-pro-sidebar-and-material-ui/

//[많이쓰는 UI] 파일 업로드 - https://as-you-say.tistory.com/380

export const SideBar = () => {
    return (
        <>
        <Bar>
        <Sidebar className="Menu">
          <Menu>
            <MenuItem className="menu1">
              <h2>Menu</h2>
            </MenuItem>
            <MenuItem
                component={<Link to="/"/>}
            > 
                Home 
            </MenuItem>
            <MenuItem
                component={<Link to="/mng-car-num" />}
            > 
                차량 등록 관리
            </MenuItem>
            <MenuItem
                component={<Link to="/logs" />}
            > 
                log 확인
            </MenuItem>
          </Menu>
        </Sidebar>
      </Bar>
    </>
    )

}


/*
export const SideBar = () => {
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const setType = (itemId) => {
        if (typeof itemId === 'object') {
          dispatch({
            type: SET_TYPE,
            item: `${itemId.item}`,
            title: `${itemId.title}`,
            isTag: false,
          });
        }
    }
  
    const { user } = useSelector((state) => state.authentication);
  
    const setArr = [];

    useEffect(() => {
        // 배열로 받은 태그목록을 배열 내 각각의 object로 변환한 뒤 아래 subNav에 전달
        if (user) {
          (user.user.tags || []).forEach((tag) => {
            const curObj = {};
            curObj.title = tag;
            curObj.itemId = `/tags/${tag}`;
            setArr.push(curObj);
          });
        }
      }, []);
    return (
        <>
        <Bar>
            <Navigation
            // you can use your own router's api to get pathname
            activeItemId="/management/members"
            onSelect={({itemId}) => {
                if (itemId !== '/tags') {
                    setType(itemId);
                  }
                  if (itemId.item !== 'main') {
                    navigate('/signin');
                  }
            }}
            items={[
            {
                title: 'Home',
                itemId: '/',
                // you can use your own custom Icon component as well
                // icon is optional
                elemBefore: () => <Icon name="inbox" />,
            },
            {
                title: '사용자 등록'
                
            },
            {
                title: '사진 업로드',
                itemId: {item:'/upload'},
                elemBefore: () => <Icon name="users" />,
                
                subNav: [
                {
                    title: 'Projects',
                    itemId: '/management/projects',
                },
                {
                    title: 'Members',
                    itemId: '/management/members',
                },
                ],
                
            },
            {
                title: '로그 확인',
                itemId: '/log',
                
                subNav: [
                {
                    title: 'Teams',
                    itemId: '/management/teams',
                },
                ],
                
            },
            ]}
            />
        </Bar>
        </>
        
    )
}
*/
