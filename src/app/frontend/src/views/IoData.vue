<template>
    <div>
        <!-- <Switch v-model="input[0].level" @on-change="change"></Switch> -->
        <h3>输入端口</h3>
        <Table border :columns="columns7" :data="input"></Table>
        <h3>输出端口</h3>
        <Table border :columns="columns7" :data="output"></Table>
        <h3>未使用端口</h3>
        <Table border :columns="columns7" :data="notset"></Table>
    </div>
</template>
<script>
    export default {
        data() {
            return {
                columns7: [
                    {
                        title: 'io编号',
                        key: 'io_number',
                        width: 90,
                        sortable: true,
                        sortType: 'asc',
                        alias: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Icon', {
                                    props: {
                                        type: 'person'
                                    }
                                }),
                                h('strong', params.row.io_number)
                            ]);
                        }
                    },
                    {
                        title: 'io名称',
                        key: 'io_name',
                        width: 160,
                        render: (h, params) => {
                            return h('input', {
                                props: {
                                    type: 'text'
                                },
                                style: {
                                    //width: '100px',
                                },
                                domProps: {
                                    value: params.row.io_name
                                },
                                on: {
                                    input: (event) => {
                                        // this.input[params.index].io_name = event.target.value;
                                        params.row.io_name = event.target.value;
                                        console.log(params.row.io_name)

                                    }
                                }
                            }, [
                                    h('strong', params.row.io_name)
                                ]);
                        }
                    },
                    {
                        title: '电平',
                        key: 'level',
                        width: 80,
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: params.row.level ? 'success' : 'error',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: (event) => {
                                            if (this.output[params.index].io_number === params.row.io_number) {
                                                params.row.level = !params.row.level;
                                                // todo: 给后台发送修改后的数据
                                                this.switchLevel(params.index)
                                            }

                                        }
                                    }
                                }, params.row.level),
                            ]);
                        }
                    },
                    {
                        title: '名称设置',
                        key: 'action',
                        width: 100,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'primary',
                                        size: 'small'
                                    },
                                    style: {
                                        marginRight: '5px'
                                    },
                                    on: {
                                        click: () => {
                                            this.changeName(params)
                                        }
                                    }
                                }, '设置名称')
                            ]);
                        }
                    },
                    {
                        title: '切换输入输出',
                        key: 'action',
                        width: 200,
                        align: 'center',
                        render: (h, params) => {
                            return h('div', [
                                h('Button', {
                                    props: {
                                        type: 'info',
                                        shape: 'circle',
                                        icon: 'code-working',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.switchIoType(params, 'input');
                                        }
                                    }
                                }, '输入'),
                                h('Button', {
                                    props: {
                                        type: 'info',
                                        shape: 'circle',
                                        icon: 'code-working',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.switchIoType(params, 'output');
                                        }
                                    }
                                }, '输出'),
                                h('Button', {
                                    props: {
                                        type: 'error',
                                        size: 'small'
                                    },
                                    on: {
                                        click: () => {
                                            this.switchIoType(params, 'notset')
                                        }
                                    }
                                }, '删除')
                            ]);
                        }
                    }
                ],
                input: [
                    {
                        io_number: 'io0',
                        io_name: '输入测试1',
                        level: true
                    },
                    {
                        io_number: 'io1',
                        io_name: '输入测试2',
                        level: false
                    },
                    {
                        io_number: 'io2',
                        io_name: '输入测试3',
                        level: true
                    },
                    {
                        io_number: 'io3',
                        io_name: '输入测试4',
                        level: false
                    },
                    {
                        io_number: 'io4',
                        io_name: '输入测试5',
                        level: true
                    },
                    {
                        io_number: 'io5',
                        io_name: '输入测试6',
                        level: false
                    },
                    {
                        io_number: 'io6',
                        io_name: '输入测试7',
                        level: true
                    }
                ],
                output: [
                    {
                        io_number: 'io8',
                        io_name: '输出测试1',
                        level: false
                    },
                    {
                        io_number: 'io9',
                        io_name: '输出测试2',
                        level: true
                    },
                    {
                        io_number: 'io10',
                        io_name: '输出测试3',
                        level: false
                    },
                    {
                        io_number: 'io11',
                        io_name: '输出测试4',
                        level: true
                    },
                    {
                        io_number: 'io12',
                        io_name: '输出测试5',
                        level: false
                    },
                    {
                        io_number: 'io13',
                        io_name: '输出测试6',
                        level: true
                    },
                    {
                        io_number: 'io14',
                        io_name: '输出测试7',
                        level: false
                    },
                ],
                notset: [
                    { io_number: 'io7' },
                    { io_number: 'io15' },
                ]
            }
        },
        mounted() {
            // get数据
            console.log('get')
        },
        methods: {
            switchLevel(index) {
                console.log("put io数据")
                // todo: 发送一下新设置的io数据
            },
            defineType(params) {
                for (var i in this.input) {
                    if (this.input[i].io_number == params.row.io_number) {
                        return 'input'
                    }
                }
                for (var i in this.output) {
                    if (this.output[i].io_number == params.row.io_number) {
                        return 'output'
                    }
                }
                return 'notset'
            },
            changeName(params) {
                var dataType = this.defineType(params);
                console.log(params);
                this[dataType][params.index].io_name = params.row.io_name;
                // todo: 给后台发送修改后的数据
            },
            switchIoType(params, aimType) {
                var dataType = this.defineType(params);
                console.log(dataType)
                console.log(aimType)
                if (dataType === aimType) {
                    console.log('====')
                    return
                } else {
                    if (aimType == 'notset') {
                        this[aimType].push({
                            io_number: params.row.io_number,
                            io_name: params.row.io_name,
                            level: ''
                        });
                        this[dataType].splice(params.index, 1);
                        console.log('set notset')
                    }
                    else {
                        this[aimType].push({
                            io_number: params.row.io_number,
                            io_name: params.row.io_name,
                            level: ''
                        });
                        this[dataType].splice(params.index, 1);
                        console.log('change')
                        console.log('del ' + dataType)
                    }
                }
                // todo: post一下修改后的设置，get一下数据
            }
        }
    }
</script>