<template>
    <div>
        <Form ref="serial-setting-data" :model="serial_device" :label-width="60" inline>
            <FormItem label="生效设备">
                <Select v-model="serial_device.active_device">
                    <Option v-for="(value, deviceName) in serial_device" v-if="deviceName !== 'active_device'" :value='deviceName'>{{deviceName}}</Option>
                </Select>
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
                <Button type="ghost" @click="handleReset('serial_device')" style="margin-left: 8px">Reset</Button>
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
                    active_device: '测试1',
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
                ruleValidate: {
                    newDeviceName: [
                        { required: true, message: '虚拟设备名称不能为空', trigger: 'blur' }
                    ],
                }
            }
        },
        mounted(){
            // get数据
            console.log('get')
        },
        methods: {
            handleSubmitActiveDevice() {
                // post一下serial_device.active_device
                console.log(this.serial_device.active_device)
            },
            handleSubmitDevice() {
                // post一下serial_device
                console.log(this.serial_device)
            },
            handleReset(name) {
                // 从设备重新获取一次数据
                console.log(JSON.stringify(this.serial_device))
                console.log(this.index)
                console.log(this.serial_device)
                console.log(this.newDeviceName)
                this.$refs[name].resetFields();
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