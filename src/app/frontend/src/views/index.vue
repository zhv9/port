<style scoped>
    .layout {
        border: 1px solid #d7dde4;
        background: #f5f7f9;
        position: relative;
        border-radius: 4px;
        overflow: hidden;
    }

    .layout-header-bar {
        background: #fff;
        box-shadow: 0 1px 1px rgba(0, 0, 0, .1);
    }
</style>
<template>
    <div class="layout">
        <Sider :style="{position: 'fixed', height: '100vh', left: 0, overflow: 'auto'}">
            <Menu active-name="1-2" theme="dark" width="auto" :open-names="['1']">
                <Submenu name="1">
                    <template slot="title">
                        <Icon size="20" type="arrow-swap"></Icon>
                        IO控制
                    </template>
                    <MenuItem name="1-1" @click.native="menuClick">
                    <Icon size="20" type="settings"></Icon>
                    配置
                    </MenuItem>
                    <MenuItem name="1-2" @click.native="menuClick">
                    <Icon size="20" type="nuclear"></Icon>
                    数据
                    </MenuItem>
                    <MenuItem name="1-3" @click.native="menuClick">
                    <Icon size="20" type="erlenmeyer-flask"></Icon>
                    其他
                    </MenuItem>
                </Submenu>
                <Submenu name="2">
                    <template slot="title">
                        <Icon size="20" type="shuffle"></Icon>
                        串口控制
                    </template>
                    <MenuItem name="2-1" @click.native="menuClick">
                    <Icon size="20" type="settings"></Icon>
                    配置
                    </MenuItem>
                    <MenuItem name="2-2" @click.native="menuClick">
                    <Icon size="20" type="nuclear"></Icon>
                    数据
                    </MenuItem>
                    <MenuItem name="2-3" @click.native="menuClick">
                    <Icon size="20" type="erlenmeyer-flask"></Icon>
                    其他
                    </MenuItem>
                </Submenu>
                <Submenu name="3">
                    <template slot="title">
                        <Icon size="20" type="android-bus"></Icon>
                        Modbus控制
                    </template>
                    <MenuItem name="3-1" @click.native="menuClick">
                    <Icon size="20" type="settings"></Icon>
                    配置
                    </MenuItem>
                    <MenuItem name="3-2" @click.native="menuClick">
                    <Icon size="20" type="nuclear"></Icon>
                    数据
                    </MenuItem>
                    <MenuItem name="3-3" @click.native="menuClick">
                    <Icon size="20" type="erlenmeyer-flask"></Icon>
                    其他
                    </MenuItem>
                </Submenu>

            </Menu>
        </Sider>
        <Layout :style="{marginLeft: '200px'}">
            <Header :style="{background: '#fff', boxShadow: '0 2px 3px 2px rgba(0,0,0,.1)'}"></Header>
            <Content :style="{padding: '0 16px 16px'}">
                <Breadcrumb :style="{margin: '16px 0'}">
                    <BreadcrumbItem>Home</BreadcrumbItem>
                    <BreadcrumbItem>{{navComponents}}</BreadcrumbItem>
                    <BreadcrumbItem>{{navLayout}}</BreadcrumbItem>
                </Breadcrumb>
                <Card>
                    <div style="height: 600px">
                        <component :is="currentView"></component>
                    </div>
                </Card>
            </Content>
        </Layout>
    </div>
</template>
<script>
    import ioSetting from './IoSetting'
    import ioData from './IoData'
    import serialSetting from './SerialSetting'
    import serialData from './SerialData'
    export default {
        data() {
            return {
                navComponents: '',
                navLayout: '',
                contents: {
                    'IO控制': {
                        '配置': ioSetting,
                        '数据': ioData,
                        '其他': 'ioOther'
                    },
                    '串口控制': {
                        '配置': serialSetting,
                        '数据': serialData,
                        '其他': 'serialOther'
                    },
                    'ModBus控制': {
                        '配置': 'modbusSetting',
                        '数据': 'modbusData',
                        '其他': 'modbusOther'
                    }
                },
                currentView: ''
            }
        },
        components: {
            ioSetting, ioData, serialSetting, serialData
        },
        methods: {
            menuClick(event) {
                var components = event.currentTarget.parentElement.parentNode.firstChild.innerText
                    .trim();
                var layout = event.currentTarget.innerText
                    .replace(/^(\s|\u00A0)+/, '').replace(/(\s|\u00A0)+$/, '');
                this.navComponents = components;
                this.navLayout = layout;
                this.currentView = this.contents[components][layout]
            }
        }
    }
</script>