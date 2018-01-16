<template>
    <div>
        <Form ref="serial-setting-data" :model="serial_device" :label-width="60" inline>
            <FormItem label="生效设备">
                <!-- 使用iview的控件并编译，选择选项后不显示内容 -->
                <select v-model="active_device" style="width:200px">
                    <option v-for="(value, deviceName) in serial_device" :value='deviceName'>{{deviceName}}</option>
                </select>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmitActiveDevice()">修改生效设备</Button>
            </FormItem>
        </Form>
        <Form ref="serial_device" :model="serial_device" :label-width="60" style="width: 800px" :rules="ruleValidate">
            <FormItem v-for="(deviceValue, deviceName, index) in serial_device" v-if="deviceName !== 'active_device'" :label="deviceName">
                <Row v-for="(device, index) in deviceValue">
                    <Col span="8">
                    <Input type="text" v-model="device.receive" placeholder="接收数据"></Input>
                    </Col>
                    <Col span="8" offset="1">
                    <Input type="text" v-model="device.send" placeholder="发送数据"></Input>
                    </Col>
                    <Col span="2" offset="1">
                    <Button type="dashed" long @click="handleAdd(deviceValue)" icon="plus-round">Add</Button>
                    </Col>
                    <Col span="2">
                    <Button type="ghost" @click="handleRemove(deviceValue, index)">Delete</Button>
                    </Col>
                </Row>
            </FormItem>
            <FormItem>
                <Row>
                    <Col span="8">
                    <Input type="text" v-model="newDeviceName" placeholder="新虚拟设备名称"></Input>
                    </Col>
                    <Col span="4" offset="6">
                    <Button type="dashed" long @click="handleAddDevice(newDeviceName)" icon="plus-round">Add Device</Button>
                    </Col>
                </Row>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmitDevice('serial_device')">提交</Button>
                <Button type="ghost" @click="handleGetDevice('serial_device')" style="margin-left: 8px">Reset</Button>
            </FormItem>
        </Form>
    </div>

</template>
<script>
    export default {
        data() {
            return {
                index: 1,
                newDeviceName: '',
                'serial_device': {
                    测试1: [
                        { receive: 'receive1\r\n', send: 'send1\r\n' },
                        { receive: 'receive2\r\n', send: 'send2\r\n' },
                        { receive: 'receive3\r\n', send: 'send3\r\n' },
                        { receive: 'receive4\r\n', send: 'send4\r\n' },
                    ],
                    测试2: [
                        { receive: 'receiveA\r\n', send: 'sendA\r\n' },
                        { receive: 'receiveB\r\n', send: 'sendB\r\n' },
                        { receive: 'receiveC\r\n', send: 'sendC\r\n' },
                    ]
                },
                active_device: '',
                ruleValidate: {
                    newDeviceName: [
                        { required: true, message: '虚拟设备名称不能为空', trigger: 'blur' }
                    ],
                }
            }
        },
        mounted() {
            this.handleGetDevice();
            this.handleGetActiveDevice();
        },
        methods: {
            handleGetDevice(name) {
                // 从设备重新获取一次数据
                console.log(JSON.stringify(this.serial_device))
                console.log(this.index)
                console.log(this.serial_device)
                console.log(this.newDeviceName)
                const path = '/api/serial/setting/device/';
                var self = this;
                var xhr = new XMLHttpRequest();
                xhr.timeout = 1000;
                xhr.open('GET', path, true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('Accept', 'application/json');
                xhr.onload = function (e) {
                    if (this.status == 200 || this.status == 304) {
                        var response = JSON.parse(this.responseText);
                        self.serial_device = response['serial_device'];
                        console.log(response);
                    }
                }
                xhr.send();

            },
            handleSubmitDevice() {
                // post一下serial_device
                console.log(this.serial_device);
                const path = '/api/serial/setting/device/';
                var self = this;
                var xhr = new XMLHttpRequest();
                xhr.timeout = 1000;
                xhr.open('POST', path, true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('Accept', 'application/json');
                xhr.onload = function (e) {
                    if (this.status == 200 || this.status == 304) {
                        var response = JSON.parse(this.responseText);
                        console.log(response);
                    }
                }
                xhr.send(JSON.stringify({ 'serial_device': self.serial_device }));
            },
            handleSubmitActiveDevice() {
                // post一下active_device
                const path = '/api/serial/setting/device/active_device/';
                var self = this;
                var xhr = new XMLHttpRequest();
                xhr.timeout = 1000;
                xhr.open('POST', path + self.active_device, true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('Accept', 'application/json');
                xhr.onload = function (e) {
                    if (this.status == 200 || this.status == 304) {
                        var response = JSON.parse(this.responseText);
                        console.log(response);
                    }
                }
                xhr.send();
                console.log(this.active_device)
            },
            handleGetActiveDevice() {
                const path = '/api/serial/setting/device/active_device/';
                var self = this;
                var xhr = new XMLHttpRequest();
                xhr.timeout = 1000;
                xhr.open('GET', path, true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.setRequestHeader('Accept', 'application/json');
                xhr.onload = function (e) {
                    if (this.status == 200 || this.status == 304) {
                        var response = JSON.parse(this.responseText);
                        self.active_device = response['active_device']

                        console.log(response);
                    }
                }
                xhr.send();
                console.log(this.serial_device.active_device)
            },
            // 给设备添加单个项目
            handleAdd(deviceValue) {
                this.index++;
                deviceValue.push({
                    receive: '',
                    send: ''

                });
            },
            // 删除一个设备的单个项目
            handleRemove(deviceValue, index) {
                deviceValue.splice(index, 1);
                if (deviceValue.length === 0) {
                    // todo: 有时间了回来看看这个是咋回事，就是不能用
                    this.serial_device.splice(this.active_device.indexOf(deviceValue), 1);
                    // this.serial_device.splice(i, 1);
                }
            },
            // 添加一个虚拟设备
            handleAddDevice(newDeviceName) {
                if (newDeviceName === '') {
                    return
                }
                this.index++;
                // serial_device.splice('newDeviceName', 1, [{
                //     send: '',
                //     receive: ''
                // }]);
                this.$set(this.serial_device, newDeviceName, [{
                    receive: '',
                    send: ''
                }]);
            }
        }
    }
</script>