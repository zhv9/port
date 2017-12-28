import sys
sys.path.append('../..')
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from hardware import io_manager
from hardware import defines

app = Flask(__name__)
api = Api(app)


class IoSetting(Resource):
    def __init__(self):
        self.my_io = io_manager.IoSetup()
        self.my_io_data = io_manager.IoData()

    def get(self):
        result = {
            'type': {'input': [], 'output': [], 'notset': []},
            'data': {}
        }
        result['type']['input'] = self.my_io.get_io_type(io_manager.IoType.input)
        result['type']['output'] = self.my_io.get_io_type(io_manager.IoType.output)
        result['type']['notset'] = self.my_io.get_io_type(io_manager.IoType.notset)

        result['data'] = self.my_io_data.get_data_list(result['type']['input'] + result['type']['output'])

        return {'io': result}


class IoSettingInput(Resource):
    def __init__(self):
        self.my_io = io_manager.IoSetup()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('input', type=[], help='将对应io设置为input类型', location='json')
        self.io_type = io_manager.IoType.input

    def get(self):
        result = self.my_io.get_io_type(self.io_type)
        return {'input': result}

    def put(self, io_number=None):
        args = self.parser.parse_args()
        if io_number is None:
            self.my_io.set_io_list(self.io_type, args['input'])
        elif io_number in defines.io_defines:
            self.my_io.set_io_type(self.io_type, io_number)
        else:
            abort(404)
        return self.get()

    def post(self, io_number=None):
        self.put(io_number)

    def delete(self, io_number=None):
        if io_number is None:
            io_output_list = self.my_io.get_io_type(self.io_type)
            for io in io_output_list:
                self.my_io.io_cleanup_setup(io)
        else:
            self.my_io.io_cleanup_setup(io_number)
        return self.get()


class IoSettingOutput(Resource):
    def __init__(self):
        self.my_io = io_manager.IoSetup()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('output', type=[], help='将对应io设置为output类型')
        self.io_type = io_manager.IoType.output

    def get(self):
        result = self.my_io.get_io_type(self.io_type)
        return {'output': result}

    def put(self, io_number=None):
        args = self.parser.parse_args()
        if io_number is None:
            self.my_io.set_io_list(self.io_type, args['output'])
        elif io_number in defines.io_defines:
            self.my_io.set_io_type(self.io_type, io_number)
        else:
            abort(404)
        return self.get()

    def post(self, io_number=None):
        self.put(io_number)

    def delete(self, io_number=None):
        if io_number is None:
            io_output_list = self.my_io.get_io_type(self.io_type)
            for io in io_output_list:
                self.my_io.io_cleanup_setup(io)
        else:
            self.my_io.io_cleanup_setup(io_number)
        return self.get()


class IoData(Resource):
    def __init__(self):
        self.my_io_setup = io_manager.IoSetup()
        self.my_io_data = io_manager.IoData()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('data', type={}, help='io数据')

    def get(self, io_number=None):
        if io_number is None:
            my_io_setup = io_manager.IoSetup()
            active_io = my_io_setup.get_io_type(io_manager.IoType.input)
            active_io.append(my_io_setup.get_io_type(io_manager.IoType.output))
            result = self.my_io_data.get_data_list(active_io)
        else:
            result = self.my_io_data.get_data(io_number)

        return {'data': result}

    def post(self):
        self.put()

    def put(self):
        args = self.parser.parse_args()
        output_io = self.my_io_setup.get_io_type(io_manager.IoType.output)
        for io_number, level in args.items():
            if io_number in output_io:
                self.my_io_data.set_output_data(io_number, level)
            else:
                abort(500)
        pass


class IoSettingEvent(Resource):
    def __init__(self):
        self.my_io_data = io_manager.IoData()
        self.parser = reqparse.RequestParser()


api.add_resource(IoSetting, '/api/io/setting/')
api.add_resource(IoSettingInput, '/api/io/setting/input/<io_number>')
api.add_resource(IoSettingOutput, '/api/io/setting/output/<io_number>')
api.add_resource(IoSettingEvent, '/api/io/setting/event/<io_number>')
api.add_resource(IoData, '/api/io/setting/data/<io_number>')

if __name__ == '__main__':
    app.run(debug=True)
