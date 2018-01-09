const routers = [
    {
        path: '/',
        meta: {
            title: 'home'
        },
        component: (resolve) => require(['./views/index.vue'], resolve)
    },
    {
        path: '/serial/setting',
        meta: {
            title: 'SerialSetting'
        },
        component: (resolve) => require(['./views/SerialSetting.vue'], resolve)
    },
    {
        path: '/serial/data',
        meta: {
            title: 'SerialData'
        },
        component: (resolve) => require(['./views/SerialData.vue'], resolve)
    }
];
export default routers;