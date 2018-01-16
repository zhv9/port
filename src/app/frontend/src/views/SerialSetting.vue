<template>
    <div>
        <Form ref="serial-setting" :model="service" :rules="ruleItem" :label-width="60" inline>
            <FormItem label="波特率">
                <Select v-model="service.baudrate" style="width:100px">
                    <Option v-for="number in baudrates" :value='number'>{{number}}</Option>
                </Select>
            </FormItem>
            <FormItem label="端口号">
                <Select v-model="service.serial_port" style="width:100px">
                    <Option v-for="portnumber in ports" :value='portnumber'>{{portnumber}}</Option>
                </Select>
            </FormItem>
            <FormItem label="读取超时" prop="timeout">
                <Input number v-model="service.read_timeout" placeholder="读取超时(ms)"></Input>
            </FormItem>
            <FormItem label="写入超时" prop="timeout">
                <Input number v-model="service.write_timeout" placeholder="写入超时(ms)"></Input>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmit('service')">提交</Button>
            </FormItem>
        </Form>
        <serial-setting-data></serial-setting-data>
    </div>
</template>
<script>
    import SerialSettingData from "./SerialSettingData"
    export default {
        data() {
            return {
                service: {
                    baudrate: '',
                    serial_port: '',
                    read_timeout: '',
                    write_timeout: ''
                },
                ruleItem: {
                    timeout: [
                        {
                            type: 'number',
                            message: '请输入数字'
                        },
                        {
                            validator(rule, value, callback, source, options) {
                                var errors = [];
                                if (!/^[a-z0-9]+$/.test(value)) {
                                    callback('请输入整数');
                                } else if (value < 10 || value > 2000) {
                                    callback('数值必须大于10，小于2000')
                                }
                                callback(errors);
                            }
                        }
                    ]
                },
                baudrates: [300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 43000, 56000, 57600, 115200],
                ports: ['com1', 'com2', 'com3']
            }
        },
        mounted() {
            // get数据
            this.getSettingService();
        },
        methods: {
            handleSubmit(name) {
                this.setSettingService();
                this.getSettingService();
            },
            getSettingService() {
                const path = '/api/serial/setting/service/';
                var self = this;
                var xhr = new XMLHttpRequest();
                xhr.timeout = 1000;
                xhr.open('GET', path, true);
                // xhr.responseType = "json";
                xhr.setRequestHeader('Access-Control-Allow-Origin', 'true')
                xhr.onload = function () {
                    var response = JSON.parse(xhr.responseText)
                    self.service = response['serial_service_setting']['service']
                }
                xhr.send();
            },
            setSettingService() {
                const path = '/api/serial/setting/service/';
                var self = this;
                var xhr = new XMLHttpRequest();
                xhr.timeout = 1000;
                xhr.open('POST', path, true);
                // xhr.responseType = "json";
                xhr.setRequestHeader('Content-Type', 'application/json')
                xhr.setRequestHeader('Accept', 'application/json')
                xhr.setRequestHeader('Access-Control-Allow-Origin', 'true')
                xhr.onload = function (e) {
                    if (this.status == 200 || this.status == 304) {
                        var response = JSON.parse(this.responseText);
                        console.log(response);
                    }
                }
                xhr.send(JSON.stringify(self.service));
            }
        },
        components: {
            SerialSettingData
        }
    }
</script>