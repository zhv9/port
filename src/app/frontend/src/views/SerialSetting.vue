<template>
    <div>
        <Form ref="serial-setting" :model="formItem" :rules="ruleItem" :label-width="60" inline>
            <FormItem label="波特率">
                <Select v-model="formItem.baudrate">
                    <Option v-for="number in baudrates" :value='number'>{{number}}</Option>
                </Select>
            </FormItem>
            <FormItem label="端口号">
                <Select v-model="formItem.port">
                    <Option v-for="portnumber in ports" :value='portnumber'>{{portnumber}}</Option>
                </Select>
            </FormItem>
            <FormItem label="读取超时" prop="timeout">
                <Input number v-model="formItem.readTimeout" placeholder="读取超时(ms)"></Input>
            </FormItem>
            <FormItem label="写入超时" prop="timeout">
                <Input number v-model="formItem.writeTimeout" placeholder="写入超时(ms)"></Input>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmit('formItem')">提交</Button>
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
                formItem: {
                    baudrate: '',
                    port: '',
                    readTimeout: '',
                    writeTimeout: ''
                },
                ruleItem: {
                    timeout: [
                        {
                            type: 'number',
                            message: '请输入数字'
                        },
                        {validator(rule, value, callback, source,options){
                            var errors = [];
                            if (!/^[a-z0-9]+$/.test(value)){
                                callback('请输入整数');
                            }else if(value<10 || value>2000){
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
        methods: {
            handleSubmit(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        this.$Message.success('Success!');
                    } else {
                        this.$Message.error('Fail!');
                    }
                })
            }
        },
        components: {
            SerialSettingData
        }
    }
</script>