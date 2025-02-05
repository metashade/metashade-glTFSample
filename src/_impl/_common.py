# Copyright 2020 Pavlo Penenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

entry_point_name = 'main'

def _generate_vs_out(sh, primitive):
    with sh.vs_output('VsOut') as VsOut:
        VsOut.SV_Position('Pclip', sh.Vector4f)
        
        VsOut.texCoord('Pw', sh.Point3f)
        VsOut.texCoord('Nw', sh.Vector3f)

        if primitive.attributes.TANGENT is not None:
            VsOut.texCoord('Tw', sh.Vector3f)
            VsOut.texCoord('Bw', sh.Vector3f)

        VsOut.texCoord('uv0', sh.Point2f)

        if primitive.attributes.COLOR_0 is not None:
            VsOut.color('rgbaColor0', sh.RgbaF)

def _generate_per_frame_uniform_buffer(sh):
    sh.struct('Light')(
        VpXf = sh.Matrix4x4f,
        ViewXf = sh.Matrix4x4f,
        v3DirectionW = sh.Vector3f,
        fRange = sh.Float,
        rgbColor = sh.RgbF,
        fIntensity = sh.Float,
        Pw = sh.Point3f,
        fInnerConeCos = sh.Float,
        fOuterConeCos = sh.Float,
        type_ = sh.Float, # should be an int, but we assume a spotlight anyway
        fDepthBias = sh.Float,
        iShadowMap = sh.Float # should be an int, unused for now
    )

    with sh.uniform_buffer(dx_register = 0, name = 'cbPerFrame'):
        sh.uniform('g_VpXf', sh.Matrix4x4f)
        sh.uniform('g_prevVpXf', sh.Matrix4x4f)
        sh.uniform('g_VpIXf', sh.Matrix4x4f)
        sh.uniform('g_cameraPw', sh.Point3f)
        sh.uniform('g_cameraPw_fPadding', sh.Float)
        sh.uniform('g_fIblFactor', sh.Float)
        sh.uniform('g_fPerFrameEmissiveFactor', sh.Float)
        sh.uniform('g_fInvScreenResolution', sh.Float2)
        sh.uniform('g_f4WireframeOptions', sh.Float4)
        sh.uniform('g_f2MCameraCurrJitter', sh.Float2)
        sh.uniform('g_f2MCameraPrevJitter', sh.Float2)

        # should be an array
        for light_idx in range(0, 80):
            sh.uniform(f'g_light{light_idx}', sh.Light)

        sh.uniform('g_nLights', sh.Float)   # should be int
        sh.uniform('g_lodBias', sh.Float)

def _generate_per_object_uniform_buffer(sh, is_ps : bool):
    if is_ps:
        sh.struct('PbrFactors')(
            rgbaEmissive = sh.RgbaF,

            # pbrMetallicRoughness
            rgbaBaseColor = sh.RgbaF,
            fMetallic = sh.Float,
            fRoughness = sh.Float,

            f2Padding = sh.Float2,

            # KHR_materials_pbrSpecularGlossiness
            rgbaDiffuse = sh.RgbaF,
            rgbSpecular = sh.RgbF,
            fGlossiness = sh.Float
        )

    with sh.uniform_buffer(dx_register = 1, name = 'cbPerObject'):
        sh.uniform('g_WorldXf', sh.Matrix3x4f)
        sh.uniform('g_prevWorldXf', sh.Matrix3x4f)
        if is_ps:
            sh.uniform('g_perObjectPbrFactors', sh.PbrFactors)
